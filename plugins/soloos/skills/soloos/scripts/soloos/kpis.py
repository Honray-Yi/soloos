"""Bounded arithmetic expressions, never eval; evidence-aware KPI computation."""

import ast
from decimal import Decimal, DecimalException, localcontext

from .catalog import TEMPLATES
from .data import trusted, validate
from .finance import calculate, money


def expression(formula, values):
    if len(formula) > 500:
        raise ValueError('Formula exceeds 500 characters')
    try:
        tree = ast.parse(formula, mode='eval')
    except (SyntaxError, RecursionError) as exc:
        raise ValueError('Invalid arithmetic formula') from exc
    if len(list(ast.walk(tree))) > 100:
        raise ValueError('Formula is too complex')
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name):
            if node.id not in values:
                raise ValueError('Undeclared input: ' + node.id)
            return Decimal(values[node.id])
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            value = Decimal(ast.get_source_segment(formula, node))
            if not value.is_finite() or abs(value) > Decimal('1e15'):
                raise ValueError('Constant outside supported range')
            return value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return left + right
            if isinstance(node.op, ast.Sub): return left - right
            if isinstance(node.op, ast.Mult): return left * right
            if right == 0: raise ValueError('Zero denominator')
            return left / right
        raise ValueError('Only names, numeric constants, +, -, * and / are supported')
    try:
        with localcontext() as context:
            context.prec = 40
            result = visit(tree)
            if not result.is_finite() or abs(result) > Decimal('1e20'):
                raise ValueError('Formula result outside supported range')
            return result
    except DecimalException as exc:
        raise ValueError('Invalid decimal arithmetic') from exc


def business_kpis(data, start, end):
    validate(data)
    financials = calculate(data, start, end)
    values = {key: (financials[key], 'money', ['cash-ledger']) for key in ('revenue', 'expenses', 'profit')}
    for row in data.get('measurements', []):
        if row['start'] == start and row['end'] == end:
            values[row['metric']] = (row['value'] if trusted(row) else None, row['unit'], [row['id']])
    definitions = TEMPLATES[data['company']['business_type']] + data.get('custom_kpis', [])
    results = {}
    for definition in definitions:
        name, inputs = definition['name'], definition['input_units']
        if name in results or name in ('revenue', 'expenses', 'profit'):
            raise ValueError('Duplicate/reserved KPI name: ' + name)
        missing = [key for key, unit in inputs.items() if key not in values or values[key][0] is None or values[key][1] != unit]
        result = {'value': None, 'unit': definition['unit'], 'formula': definition['formula'],
                  'description': definition['description'], 'status': 'unavailable', 'missing_inputs': missing,
                  'provenance': [item for key in inputs if key in values for item in values[key][2]]}
        if not missing:
            try:
                value = expression(definition['formula'], {key: values[key][0] for key in inputs})
                result.update(value=money(value, data['company']['minor_units'] if definition['unit'] == 'money' else 6), status='calculated')
            except ValueError as exc:
                result['reason'] = str(exc)
        results[name] = result
    return {'financials': financials, 'business_type': data['company']['business_type'], 'metrics': results}
