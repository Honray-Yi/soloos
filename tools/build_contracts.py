"""Build v1 additive data contracts from the reviewed Phase 1 schema.

Run against a staging skill; generated JSON schemas ship with the runtime.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path


def build(root):
    path = root / 'assets/business.schema.json'
    schema = json.loads(path.read_text(encoding='utf-8'))
    schema['properties']['schema_version'] = {'enum': ['0.1', '1.0']}
    schema['title'] = 'SoloOS business dataset v1 (backward compatible with 0.1)'
    text = {'type': 'string', 'minLength': 1}
    number = {'type': 'string', 'pattern': r'^-?(0|[1-9][0-9]{0,14})(\.[0-9]{1,6})?$'}
    def obj(properties, required=None):
        return {'type': 'object', 'additionalProperties': False, 'properties': properties,
                'required': required if required is not None else list(properties)}
    common = {'id': text, 'company_id': text, 'record_type': text,
              'metadata': {'$ref': '#/$defs/metadata'}}
    models = {
        'Goal': {'name': text, 'metric': text, 'target': number, 'direction': {'enum': ['at_least', 'at_most']}, 'due_date': {'type': 'string', 'format': 'date'}},
        'Project': {'name': text, 'status': {'enum': ['planned', 'active', 'blocked', 'done']}, 'goal_id': text},
        'Task': {'name': text, 'project_id': text, 'owner': text, 'status': {'enum': ['todo', 'doing', 'blocked', 'done']}, 'due_date': {'type': 'string', 'format': 'date'}},
        'Customer': {'name': text, 'stage': {'enum': ['lead', 'qualified', 'won', 'lost', 'active', 'churned']}, 'value': {'$ref': '#/$defs/money'}},
        'Product': {'name': text, 'price': {'$ref': '#/$defs/money'}, 'unit_cost': {'$ref': '#/$defs/money'}, 'status': {'enum': ['idea', 'building', 'active', 'retired']}},
        'Campaign': {'name': text, 'product_id': text, 'channel': text, 'budget': {'$ref': '#/$defs/money'}, 'status': {'enum': ['planned', 'active', 'paused', 'complete']}},
    }
    for kind, fields in models.items():
        schema['$defs'][kind] = obj({**deepcopy(common), 'record_type': {'const': kind}, **fields})
    schema['properties']['entities'] = {'type': 'array', 'items': {'oneOf': [{'$ref': '#/$defs/' + kind} for kind in models]}}
    schema['$defs']['measurement'] = obj({**deepcopy(common), 'record_type': {'const': 'Measurement'},
        'metric': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]{0,63}$'}, 'value': number,
        'unit': {'enum': ['money', 'count', 'hours', 'ratio', 'number']},
        'start': {'type': 'string', 'format': 'date'}, 'end': {'type': 'string', 'format': 'date'}})
    schema['properties']['measurements'] = {'type': 'array', 'items': {'$ref': '#/$defs/measurement'}}
    schema['$defs']['custom_kpi'] = obj({'name': {'type': 'string', 'pattern': '^[a-z][a-z0-9_]{0,63}$'},
        'formula': {'type': 'string', 'minLength': 1, 'maxLength': 500},
        'input_units': {'type': 'object', 'minProperties': 1, 'additionalProperties': {'enum': ['money', 'count', 'hours', 'ratio', 'number']}},
        'unit': {'enum': ['money', 'count', 'hours', 'ratio', 'number']}, 'description': text})
    schema['properties']['custom_kpis'] = {'type': 'array', 'items': {'$ref': '#/$defs/custom_kpi'}}
    path.write_text(json.dumps(schema, indent=2) + '\n', encoding='utf-8')
    output_path = root / 'assets/output.schema.json'
    output = json.loads(output_path.read_text(encoding='utf-8'))
    output['properties']['schema_version'] = {'enum': ['0.1', '1.0']}
    output['properties']['record_type'] = {'enum': ['Report', 'Decision', 'Forecast', 'Outcome']}
    output['allOf'][0]['then']['properties']['payload']['properties']['cadence'] = {'enum': ['daily', 'weekly', 'monthly', 'quarterly', 'annual']}
    output['allOf'] = output['allOf'][:2] + [
        {'if': {'properties': {'record_type': {'const': kind}}}, 'then': {'properties': {'payload': {'required': fields}}}}
        for kind, fields in [('Forecast', ['baseline','assumptions','status','months']), ('Outcome', ['decision_id','metric','target','actual','assessment'])]
    ]
    report_properties = output['allOf'][0]['then']['properties']['payload']['properties']
    nullable_number = {'anyOf': [number, {'type':'null'}]}
    report_properties['kpis']['properties'] = {key: deepcopy(nullable_number) for key in ['revenue','expenses','profit','runway_months']}
    report_properties['kpis']['properties']['complete'] = {'type':'boolean'}
    output_path.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    action_path = root/'assets/action.schema.json'
    if action_path.exists():
        action = json.loads(action_path.read_text(encoding='utf-8'))
        action['$defs'] = {'metadata': deepcopy(schema['$defs']['metadata'])}
        action['properties']['metadata'] = {'$ref':'#/$defs/metadata'}
        if 'metadata' not in action['required']: action['required'].append('metadata')
        action_path.write_text(json.dumps(action,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('skill', type=Path)
    build(parser.parse_args().skill)
