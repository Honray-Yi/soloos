from copy import deepcopy
from decimal import Decimal
import pytest

from soloos.catalog import TEMPLATES, DEPARTMENTS
from soloos.data import validate
from soloos.kpis import business_kpis, expression
from soloos.management import department_review
from soloos.routing import route


def measurement(business, name, value, unit='count'):
    return {'id': name, 'company_id': business['company']['id'], 'record_type': 'Measurement',
            'metric': name, 'value': value, 'unit': unit, 'start': '2026-11-02', 'end': '2026-11-08',
            'metadata': deepcopy(business['company']['metadata'])}


@pytest.mark.parametrize('kind,inputs,expected', [
    ('saas', {'closing_mrr': ('1200','money'), 'opening_mrr': ('1000','money'), 'lost_customers': ('2','count'), 'opening_customers': ('20','count')}, {'mrr_growth':'0.200000','customer_churn':'0.100000'}),
    ('ecommerce', {'order_revenue': ('1000','money'), 'orders': ('20','count'), 'returned_orders': ('2','count')}, {'average_order_value':'50.00','return_rate':'0.100000'}),
    ('creator', {'new_paid_members': ('10','count'), 'eligible_audience': ('200','count'), 'membership_revenue': ('1000','money'), 'paid_members': ('50','count')}, {'paid_conversion':'0.050000','revenue_per_member':'20.00'}),
    ('freelance', {'billable_hours': ('20','hours'), 'available_hours': ('40','hours'), 'service_revenue': ('1000','money')}, {'utilization':'0.500000','effective_hourly_revenue':'50.00'}),
    ('consulting', {'project_revenue': ('1000','money'), 'delivery_cost': ('400','money'), 'billable_hours': ('20','hours'), 'available_hours': ('40','hours')}, {'project_margin':'0.600000','utilization':'0.500000'}),
    ('digital-products', {'purchases': ('20','count'), 'qualified_visits': ('400','count'), 'refunded_purchases': ('2','count')}, {'purchase_conversion':'0.050000','refund_rate':'0.100000'}),
])
def test_six_templates(business, kind, inputs, expected):
    business['company']['business_type'] = kind
    business['measurements'] = [measurement(business, key, *value) for key, value in inputs.items()]
    actual = business_kpis(business, '2026-11-02', '2026-11-08')['metrics']
    assert {key: value['value'] for key, value in actual.items()} == expected


@pytest.mark.parametrize('formula', ['__import__("os")', 'a ** 100', 'a[0]', '(lambda: 1)()', 'True', '1e999', 'a//2'])
def test_formula_cannot_run_code(formula):
    with pytest.raises(ValueError): expression(formula, {'a': '1'})


def test_custom_kpi_and_zero_denominator(business):
    business['custom_kpis'] = [{'name': 'cash_margin', 'formula': 'profit/revenue', 'input_units': {'profit':'money','revenue':'money'}, 'unit': 'ratio', 'description': 'Cash profit margin'}]
    assert business_kpis(business, '2026-11-02', '2026-11-08')['metrics']['cash_margin']['value'] == '-0.350000'
    business['transactions'] = []
    assert business_kpis(business, '2026-11-02', '2026-11-08')['metrics']['cash_margin']['reason'] == 'Zero denominator'


def test_missing_untrusted_and_wrong_unit_measurements(business):
    business['measurements'] = [measurement(business, 'billable_hours', '20', 'count')]
    result = business_kpis(business, '2026-11-02', '2026-11-08')['metrics']['utilization']
    assert result['value'] is None and 'billable_hours' in result['missing_inputs']
    business['measurements'][0]['unit'] = 'hours'
    business['measurements'][0]['metadata']['evidence'] = 'forecast'
    assert business_kpis(business, '2026-11-02', '2026-11-08')['metrics']['utilization']['value'] is None


def test_relationships_and_department_priorities(business):
    base = {'company_id': business['company']['id'], 'metadata': deepcopy(business['company']['metadata'])}
    business['entities'] = [
        {**base, 'id':'g', 'record_type':'Goal', 'name':'Revenue', 'metric':'revenue', 'target':'2000', 'direction':'at_least', 'due_date':'2026-11-30'},
        {**base, 'id':'p', 'record_type':'Project', 'name':'Delivery', 'goal_id':'g', 'status':'blocked'},
        {**base, 'id':'t', 'record_type':'Task', 'name':'Launch', 'project_id':'p', 'owner':'founder', 'status':'todo', 'due_date':'2026-11-01'},
        {**base, 'id':'c', 'record_type':'Customer', 'name':'Synthetic lead', 'stage':'qualified', 'value':'2000'},
    ]
    result = department_review(business, '2026-11-02', '2026-11-08')
    assert set(result['departments']) == set(DEPARTMENTS)
    assert result['overdue_task_ids'] == ['t'] and len(result['priorities']) == 2
    business['entities'][2]['project_id'] = 'missing'
    with pytest.raises(ValueError): validate(business)


def test_measurements_cannot_replace_financial_truth(business):
    business['measurements'] = [measurement(business, 'revenue', '999999', 'money')]
    with pytest.raises(ValueError): validate(business)


def test_all_department_routes_exist():
    combined = set()
    for intent in ['strategy','sales-pipeline','operations','product','partnership','data-quality']:
        combined.update(route(intent)['departments'])
    assert combined == set(DEPARTMENTS)
