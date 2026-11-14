# Phase 1 verification — 2026-11-14

## Tested locally
Environment: Windows, CPython 3.12.14, pytest 9.2.0, jsonschema 4.26.0,
tzdata 2026.6 and PyYAML 6.0.3, isolated in the repository's ignored `.venv`.
The system Python launcher was broken; the Codex bundled Python initialized this
environment. Installation commands required host permission for temporary files/network.

Final command: `.venv/Scripts/python.exe -B -m pytest --basetemp=work/pytest-installed -q`.
Result: **90 passed**. The installed `.agents/skills/soloos` runtime was the import target.
The skill-creator `quick_validate.py` also returned **Skill is valid!**.

Coverage includes:
- Decimal aggregation, refunds, financing exclusion, zero cash, no positive burn,
  month-normalized runway and local timezone boundaries.
- Incomplete periods, unverified company/transactions, forecast exclusion, stale,
  future or missing cash snapshots and exact seven-day report periods.
- Invalid money, dates and offsets, currency/timezone mismatch, wrong company,
  duplicate transaction IDs and JSON keys, unknown fields and missing provenance.
- Marketing assumptions, break-even arithmetic, profitable baselines and invalid inputs.
- External execution refusal with absent, boolean and forged approval objects;
  separate approval classification for high-risk actions.
- Exact intent routing, unknown intents, report lineage, output validation and
  non-overwriting CLI exports.
- Standalone copied-skill subprocess execution outside the development repository.
- Skill frontmatter, metadata, reference paths and shared schema metadata definitions.

End-to-end installed CLI smoke test initialized and validated the fictional dataset,
calculated KPIs and saved [weekly report](examples/weekly-report.md) and
[marketing decision](examples/marketing-decision.json). Confirmed sample arithmetic:
MYR 2,000 revenue, 2,700 expenses, -700 profit, 3,000 normalized monthly operating
burn and 4.00 months runway. MYR 600 extra monthly spend gives 3.33 months downside
runway and MYR 1,000 required incremental revenue at assumed 60% contribution margin.

## Defect found and corrected
Initial run: 80 passed, 2 failed. jsonschema accepted invalid/naive date-time values
without its optional format dependency. Added a standard-library RFC3339 checker,
then expanded regressions for invalid offsets and canonical reporting dates.
All tests passed after the correction and again from the installed runtime.

## Reviewed, not host-certified
Reviewed progressive disclosure, provenance rules, capability fallback, proposal-only
instructions and the official skill conventions. No independent LLM behavioral trial
or live ChatGPT installation test was performed. Tests establish the Python runtime's
behavior, not that every model or host will always follow instructions.

GitHub Actions is configured for Windows/Linux and Python 3.11–3.13, but has not run
remotely; only the local environment above is verified. There is no public release,
plugin package, execution connector, scheduler or SQLite adapter in Phase 1.
Structural validation does not prove business facts; source reconciliation remains
necessary. No claim of production certification or flawless behavior is made.
