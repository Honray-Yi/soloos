"""Business-specific metric definitions: input units and formulas are explicit."""

DEPARTMENTS = {
    'CEO': ('Strategy and capital allocation', ['CFO', 'COO'], 'Choose the next constraint to resolve; compare alternatives and founder capacity.'),
    'CFO': ('Cash, profitability and funding', ['CEO', 'Sales'], 'Reconcile cash evidence, obligations and downside exposure before commitments.'),
    'CMO': ('Demand generation and attribution', ['Sales', 'CFO'], 'Test channel economics and attribution before scaling spend.'),
    'Sales': ('Pipeline and customer conversion', ['CMO', 'COO'], 'Identify the next qualified opportunity and confirm delivery capacity.'),
    'COO': ('Delivery and process reliability', ['Sales', 'CTO/Product'], 'Resolve blocked or overdue work and reduce repeatable delivery bottlenecks.'),
    'CTO/Product': ('Product value and technical delivery', ['COO', 'CEO'], 'Prioritize customer evidence, reliability and smallest useful product increment.'),
    'HR/Partnership': ('Founder capacity and partner coordination', ['COO', 'CFO'], 'Compare build, buy and partner options; verify scope, cost and available hours.'),
    'BI': ('Evidence quality and measurement', ['CFO', 'CMO'], 'Reconcile provenance, coverage and definitions before interpreting performance.'),
}


def metric(name, formula, units, unit, description):
    return dict(name=name, formula=formula, input_units=units, unit=unit, description=description)


TEMPLATES = {
    'saas': [metric('mrr_growth', '(closing_mrr-opening_mrr)/opening_mrr', {'closing_mrr': 'money', 'opening_mrr': 'money'}, 'ratio', 'Change in recurring monthly revenue; not cash receipts.'),
             metric('customer_churn', 'lost_customers/opening_customers', {'lost_customers': 'count', 'opening_customers': 'count'}, 'ratio', 'Customer losses relative to customers at period start.')],
    'ecommerce': [metric('average_order_value', 'order_revenue/orders', {'order_revenue': 'money', 'orders': 'count'}, 'money', 'Sales revenue per order under a consistent order definition.'),
                  metric('return_rate', 'returned_orders/orders', {'returned_orders': 'count', 'orders': 'count'}, 'ratio', 'Returned orders divided by orders in the same cohort/window.')],
    'creator': [metric('paid_conversion', 'new_paid_members/eligible_audience', {'new_paid_members': 'count', 'eligible_audience': 'count'}, 'ratio', 'New paid members divided by measured eligible audience.'),
                metric('revenue_per_member', 'membership_revenue/paid_members', {'membership_revenue': 'money', 'paid_members': 'count'}, 'money', 'Membership revenue per measured paid member.')],
    'freelance': [metric('utilization', 'billable_hours/available_hours', {'billable_hours': 'hours', 'available_hours': 'hours'}, 'ratio', 'Billable hours as a share of founder availability.'),
                  metric('effective_hourly_revenue', 'service_revenue/billable_hours', {'service_revenue': 'money', 'billable_hours': 'hours'}, 'money', 'Service revenue per billable hour, not hourly profit.')],
    'consulting': [metric('project_margin', '(project_revenue-delivery_cost)/project_revenue', {'project_revenue': 'money', 'delivery_cost': 'money'}, 'ratio', 'Project contribution before unallocated overhead.'),
                   metric('utilization', 'billable_hours/available_hours', {'billable_hours': 'hours', 'available_hours': 'hours'}, 'ratio', 'Delivered billable hours divided by available delivery hours.')],
    'digital-products': [metric('purchase_conversion', 'purchases/qualified_visits', {'purchases': 'count', 'qualified_visits': 'count'}, 'ratio', 'Purchases divided by measured qualified visits.'),
                         metric('refund_rate', 'refunded_purchases/purchases', {'refunded_purchases': 'count', 'purchases': 'count'}, 'ratio', 'Refunded purchases as a share of the matched purchase cohort.')],
    'custom': [],
}
