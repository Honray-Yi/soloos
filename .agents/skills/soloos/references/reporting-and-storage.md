# Reporting, scenarios and durable records

`report DATA --cadence daily|weekly|monthly|quarterly|annual --anchor YYYY-MM-DD`
selects the full company-local calendar period containing the anchor. Weeks are
Monday–Sunday; quarters are calendar quarters. Use `--format json` for the validated
record or default Markdown for the executive view. A partial current period does not
become a full-period actual: unavailable KPIs and evidence gaps remain explicit.
Legacy `weekly-report --start --end` accepts any exact seven-day inclusive interval.
There is no scheduler. Run reports on demand or through a separately configured host
automation; report generation never proves a future schedule exists.

`forecast DATA --start DATE --end DATE --months 3 --revenue-growth 0.02
--expense-growth 0.01` produces a constant-rate scenario after the baseline. It uses
30-day months and compounds the explicit growth assumptions; it is not a learned
forecast or calendar-month plan. Growth inputs range from -1 to 1 per month and the
horizon from 1 to 24 months. Missing actuals/current closing cash withhold the scenario.
Negative projected cash is a funding gap. Future financing, debt, taxes and seasonality
must be examined separately and not silently assumed covered.

`store-put FILE --db PATH` saves a validated dataset, Report, Decision, Forecast or
Outcome as an immutable SHA-256 snapshot. `history --db PATH [--company-id ID]`
lists entries. `store-get DIGEST --db PATH --out NEW_FILE` exports a checked snapshot.
The same content deduplicates; changed content is a new snapshot. Reads do not create
a database. Store the decision before judging its outcome; conversation is not storage.

`outcome DECISION_JSON DATA --metric NAME --start DATE --end DATE --target NUMBER
--direction at_least|at_most` compares a confirmed measurement with a user-selected
criterion and retains decision/dataset provenance. It does not prove causality or
that a target was committed before the decision. Save the resulting Outcome to the
same store. Review a failure as evidence for a narrow process improvement, not a
reason to let the skill change itself or its permission policy.

SQLite is optional and local, not a hosted backend. Back up user-selected data and
journal files securely; they are not encrypted by SoloOS and should not be committed.
