# Business templates and custom KPIs

`template TYPE` returns exact formulas, declared input units and descriptions. The
six templates are SaaS, e-commerce, creator, freelance, consulting and digital products.
Use `custom` for a company requiring only universal financial and founder-defined KPIs.
Use `business-kpis DATA --start DATE --end DATE` to calculate the selected template.

| Type | Input measurements | Calculated metrics |
| --- | --- | --- |
| saas | opening_mrr, closing_mrr; opening_customers, lost_customers | MRR growth; customer churn |
| ecommerce | order_revenue, orders, returned_orders | Average order value; return rate |
| creator | new_paid_members, eligible_audience; membership_revenue, paid_members | Paid conversion; revenue per member |
| freelance | service_revenue, billable_hours, available_hours | Effective hourly revenue; utilization |
| consulting | project_revenue, delivery_cost; billable_hours, available_hours | Project contribution margin; utilization |
| digital-products | purchases, qualified_visits, refunded_purchases | Purchase conversion; refund rate |

Measurements must have confirmed/validated metadata, company ID, matching start/end,
and the declared money/count/hours/ratio/number unit. Cohorts and definitions must be
consistent: a refund counted this month may belong to an earlier order cohort. The
runtime does not discover that attribution for the founder. Rates are fractions
(0.1 = 10%). The denominator must be nonzero. No invented benchmark is imposed.

Financial revenue/expenses/profit are reserved and cannot be replaced by measurement
rows. MRR is a recurring-revenue measurement, not a synonym for cash receipts.
Project delivery cost is not automatically all company operating expense.

For custom metrics, add `custom_kpis` objects with name, formula, input_units, unit
and description. Example: formula `profit/revenue`, inputs `{profit: money,
revenue: money}`, unit `ratio`. Only bounded arithmetic with names, numeric constants,
parentheses and + - * / is permitted. No Python functions, attributes, indexing or
eval. Custom output units are founder declarations; formula dimensional meaning is
not automatically proven. Keep names distinct from template and financial metrics.
