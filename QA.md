# SoloOS release verification

## Release closure and prompt edition — 2026-11-15

The corrected v1 release passed **150 local tests**. All six Windows/Linux and
Python 3.11–3.13 CI jobs succeeded for commit
`5ea1144e0495a36f040f5a53a53e71066ad17313`:
https://github.com/Honray-Yi/soloos/actions/runs/43614128409
This confirms the line-ending/checksum defect was corrected across the matrix.

The separate `prompt-edition/` contains text-only startup instructions, shared
principles, a company profile, editable personalization settings, eight role files,
three workflows, two record/hand-off templates and one fictional quick-start case.
Content review checked role-specific responsibilities, shared evidence, conflict
handling, customization boundaries, and honest limits around tools, memory and
execution. No live cross-model behavioral evaluation is claimed for these prompts.

Repository organization is documented in REPOSITORY_MAP.md and examples/README.md.
`tools/check_repository.py` checks distributable paths and local Markdown link targets;
it does not validate external links, every Markdown anchor or model behavior. CI now
runs that check after the software tests. Generated plugin/runtime equality remains
covered by the packaging suite; local environments, journals and build ZIPs stay ignored.

## Version 1.0 — 2026-11-14

Installed-runtime validation initially passed **149 tests** on Windows with Python 3.12.14.
Command: `.venv/Scripts/python.exe -B -m pytest --basetemp=work/pytest-release-installed-final -q`.
The skill-creator validator also returned **Skill is valid!**.

Added coverage includes all six business templates, eight distinct department findings,
custom-formula rejection of code execution, entity references, report calendar/leap-year
boundaries, incomplete periods, cash scenarios, immutable SQLite snapshots, tampering
detection and decision outcomes. All original Phase 1 regressions continue to pass.

Execution tests cover default dry-run without side effects, missing/mismatched/expired
approvals, separate high-risk approval, changed targets and content, missing credentials,
unsupported operation types, HTTP contracts and redirect refusal. Duplicate and
concurrent requests are suppressed; uncertain outcomes block automatic retries and
do not log raw exception secrets. No real business issue was created for testing.

Package validation uses the official Agent Plugins 1.0 schema. Tests verify generated
package/runtime equality, checksums, deterministic ZIPs and extracted CLI execution.
`codex plugin marketplace add . --json` registered the local private source;
`codex plugin list --marketplace soloos-private --available --json` returned
`soloos@soloos-private`, version 1.0.0, available and not automatically enabled.

End-to-end v1 examples include a consulting dataset, eight-department review, weekly
executive report, cash scenario and decision outcome. The example exposes blocked
delivery and qualified pipeline together, 60% project margin, 60% utilization and a
confirmed synthetic outcome above its user-selected target.

Release CI is verified separately after upload. Live ChatGPT installation/behavior,
live provider-write acceptance, multi-user identity and tamper-proof auditing are not
claimed. This release has no automatic scheduler or public distribution authorization.

The first v1 CI run found a packaging checksum defect: text line endings changed
between Windows preparation and GitHub/Linux checkout. 148 other tests passed on
the failing runner. Fixed the builder to normalize text before hashing, added LF
repository attributes and a Windows-versus-Unix reproducibility regression. The
corrected suite contains 150 tests; final matrix results follow the fix commit.

## Historical Phase 1 verification — 2026-11-14

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

GitHub Actions completed successfully on Windows/Linux and Python 3.11–3.13:
all six matrix jobs passed for commit `4159d30cada363f60d48dd95795aba9f8d4e5c3f`.
Evidence: https://github.com/Honray-Yi/soloos/actions/runs/43577214920
The private repository contains the 47 prepared source, test and documentation files.
No open-source license was added, per owner preference. There is no public release,
plugin package, execution connector, scheduler or SQLite adapter in Phase 1.
Structural validation does not prove business facts; source reconciliation remains
necessary. No claim of production certification or flawless behavior is made.
