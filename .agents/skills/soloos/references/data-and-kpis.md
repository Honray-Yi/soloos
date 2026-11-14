# Evidence and financial contracts

`assets/business.schema.json` is Draft 2020-12, accepting v1 and legacy 0.1 datasets.
`validate` checks structural and
semantic consistency; it does not authenticate source documents. Keep source records
and provenance under the founder's control. All data in the included fixture is fictional.

Every record has source, recorded_at (offset-aware timestamp), reporting currency,
IANA timezone, validation_status, evidence and provenance. Keep the original timestamp
offset on transactions; grouping uses the company reporting timezone. Use normalized
reporting currency for all records; mixed currencies are rejected rather than converted.
`minor_units` explicitly defines decimal precision; verify it for the selected currency.
Amounts are unsigned decimal strings; kind controls direction. Refunds have distinct
kinds. Financing is separately aggregated and excluded from profit and operating burn.
Only confirmed, validated transactions contribute to observed actuals.

Revenue = receipts minus revenue refunds. Expenses = payments minus expense refunds.
Profit = revenue minus expenses. These are cash-basis management metrics, not accrual
accounts, taxable income, gross margin or recognized revenue. Do not mix invoices due
with settled cash transactions. For compound transactions, normalize to unique rows.

Coverage dates are inclusive. Complete KPIs require confirmed, validated company and
coverage records, full period coverage and no excluded in-period records. Otherwise,
authoritative revenue/expenses/profit are null and partial observed totals are labeled.
A confirmed complete empty ledger means zero activity; an empty unconfirmed ledger does not.
Duplicate transaction IDs are rejected. Different IDs with duplicated source evidence
still need human reconciliation; no automatic bank reconciliation exists.

Monthly operating burn = max(expenses - revenue, 0) * 30 / inclusive period days.
Runway = available end-of-period cash / positive monthly burn. Use an independently
confirmed snapshot dated exactly at report end; do not add period flows to that snapshot.
Zero cash gives zero reserve runway. Nonpositive burn gives null with an explicit status,
not an infinity claim. Use full-precision Decimal internally and round display values
half-up; required break-even revenue rounds upward to the currency's minor unit.
Runway is an estimate, omitting future debt service, financing, seasonality and commitments.

Generated Report and Decision envelopes carry dataset SHA-256 provenance, creation
time, currency, timezone, evidence class and deterministic content IDs. IDs detect equal
proposals; they are not authorization tokens or execution idempotency guarantees.
Output validation uses `records.validate_record` and the standalone
`assets/output.schema.json`; it makes no remote schema fetches. Both schemas share
the same metadata contract, checked by a regression test.

## Operational records
Optional `entities` contains Goal, Project, Task, Customer, Product and Campaign
records. Company and Transaction retain the baseline structure; Report and Decision
are output envelopes. Forecast and Outcome are additional generated record types.
Entity IDs are unique across the dataset, company IDs must match, and goal/project/
product references must resolve to the correct record type. Preserve original records
when saving changed snapshots; there is no silent migration or overwrite.

Optional `measurements` holds named period observations, each with units and metadata.
The runtime rejects duplicate metric-period rows and reserved financial names. An
unverified observation cannot drive a calculated KPI or confirmed decision outcome.
Entity findings are current snapshot observations, not a historical events model.
