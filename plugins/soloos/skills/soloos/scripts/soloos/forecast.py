"""Explicit constant-rate cash scenarios; never a learned prediction."""
from decimal import Decimal, InvalidOperation
from .data import trusted, fingerprint
from .finance import calculate, money
from .periods import period
from .records import record


def rate(value, label):
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(label + ' must be decimal') from exc
    if not result.is_finite() or not Decimal('-1') <= result <= Decimal('1'):
        raise ValueError(label + ' must be between -1 and 1 per month')
    return result


def cash_forecast(data, start, end, months=3, revenue_growth='0', expense_growth='0'):
    k = calculate(data, start, end)
    if type(months) is not int or not 1 <= months <= 24:
        raise ValueError('Forecast horizon must be 1 to 24 months')
    revenue_rate, expense_rate = rate(revenue_growth, 'Revenue growth'), rate(expense_growth, 'Expense growth')
    snapshot = data.get('cash_snapshot')
    assumptions = {'revenue_growth_per_month': str(revenue_rate), 'expense_growth_per_month': str(expense_rate),
                   'month_basis_days': 30, 'financing': 'excluded', 'tax_and_debt_commitments': 'not separately modeled'}
    result = {'record_type': 'Forecast', 'company_id': data['company']['id'], 'evidence': 'forecast',
              'currency': k['currency'], 'timezone': k['timezone'], 'baseline': {'start': start, 'end': end},
              'provenance': ['dataset:sha256:' + fingerprint(data)], 'assumptions': assumptions,
              'status': 'unavailable', 'months': [], 'warnings': k['warnings']}
    if not k['complete'] or not snapshot or not trusted(snapshot) or snapshot['as_of'] != end:
        result['reason'] = 'Complete actuals and a confirmed closing cash snapshot are required'
        return record('Forecast', data, result, 'forecast')
    cash = Decimal(snapshot['available_cash'])
    revenue = Decimal(k['revenue']) * 30 / k['days']
    expenses = Decimal(k['expenses']) * 30 / k['days']
    minor = data['company']['minor_units']
    result['status'] = 'scenario'
    for month in range(1, months + 1):
        revenue *= 1 + revenue_rate
        expenses *= 1 + expense_rate
        cash += revenue - expenses
        result['months'].append({'month_index': month, 'revenue': money(revenue, minor), 'expenses': money(expenses, minor),
                                 'closing_cash': money(cash, minor), 'cash_shortfall': cash < 0})
    result['warnings'].append('Scenario periods are successive 30-day months after baseline end, not calendar-month predictions. Negative balances represent funding gaps.')
    return record('Forecast', data, result, 'forecast')
