# SoloOS 1.0 architecture

## Boundaries and flow
The canonical runtime is `.agents/skills/soloos`. Tests, development tooling, repository
documentation and packaging sources remain outside it. The generated plugin contains
an identical runtime under `skills/soloos`; checksums and a regression test detect drift.

Host capability detection -> intent selection -> validated records -> deterministic
metrics -> department judgment/report/proposal -> optional user-requested persistence.
External execution is a separate explicitly opted-in path requiring approvals and a
capable connector. The model never computes authoritative financial totals in place of
the runtime or infers tool capability from the host name.

## Data model
Draft 2020-12 schemas accept existing 0.1 datasets and additive 1.0 fields. No automatic
destructive migration occurs. Company and Transaction retain their original shape;
operational records are typed members of `entities`. Measurements are optional
period observations. The same source, timestamp, currency, timezone, validation status,
evidence and provenance contract applies across business records.

| Record | Implemented relationship |
| --- | --- |
| Company | Reporting currency, minor units, timezone, business model |
| Goal | Metric, target, direction and due date |
| Project | Company and Goal reference |
| Task | Project reference, owner, status and due date |
| Transaction | Company, settled cash kind, amount and timestamp |
| Customer | Company, pipeline stage and observed value |
| Product | Company, status, price and unit cost |
| Campaign | Product reference, channel, budget and status |
| Decision | Proposed management decision and input dataset lineage |
| Report | Period, KPIs, department findings and priorities |

Forecast and Outcome are additional generated envelopes. Action proposals have a
separate strict schema, content fingerprint and idempotency key. Their nonmonetary
GitHub operation uses currency XXX (not applicable). Schema checks do not authenticate
business facts. The caller must reconcile source evidence and currency definitions.

## Deterministic modules
- `data`: structural/semantic validation, duplicate keys/IDs, reference integrity.
- `finance`: Decimal cash-basis arithmetic, refund treatment and conditional runway.
- `catalog/kpis`: six model templates and bounded AST arithmetic without eval.
- `management/routing`: eight distinct department findings and exact-label routing;
  host reasoning handles natural-language intent.
- `periods/reporting`: five full calendar cadences plus legacy seven-day reports.
- `forecast`: explicit compounded 30-day scenarios; never a statistical prediction.
- `records/outcomes`: provenance envelopes and observation-versus-target evaluation.
- `storage`: optional SQLite immutable snapshots and decision history.

Counts, hours, currency precision and reporting periods are validated. Unverified or
missing inputs cannot be silently presented as actuals. Custom output units remain
user declarations; dimensional meaning and causal attribution are not automatically
proven. Entity lists are current snapshots, not a historical events warehouse.

## Authorized operations
`actions` manages action validation, approval expiry, consumption, SQLite journal
state and auditing. `connectors` contains one optional actual GitHub REST adapter.
`action_commands` separates proposal, human approval and execution.

Every issue is conservatively high risk, even if private. Two separately recorded
approvals bind the full action digest. Approval issuance requires an interactive
terminal and exact confirmation; the agent must not type it on the founder's behalf.
Credentials are read only from SOLOOS_GITHUB_TOKEN. Read-only/dry-run is the default.
Other operation kinds remain unimplemented proposals.

The journal reserves a unique key in a transaction before any HTTP request. Success
returns a provider ID; repeat attempts return the saved result. Uncertain/in-flight
attempts block retries. GitHub has no guaranteed exactly-once issue creation in this
adapter. Human reconciliation uses the request marker and journal. Redirects are
refused and no automatic HTTP retries occur. Raw exception messages are not logged.

The local user and processes with filesystem access are inside the trust boundary.
The journal is not encrypted, tamper-proof or a verified identity service. Actor names
are labels; OS permissions and credential scope protect the runtime. No host-MCP-to-
journal bridge is pretended to exist.

## Distribution and host boundaries
The plugin uses a root Agent Plugins 1.0 manifest with OpenAI UI metadata. No server,
MCP stub or hooks are bundled. A repo-local catalog exposes it as an available plugin.
Codex marketplace discovery has been verified. Advisory instructions work without
Python, but deterministic execution requires the dependencies and file capabilities.
Live ChatGPT install/behavior tests remain distinct from package and CLI tests.

No scheduler, mandatory paid API, hosted database, FX service, accrual ledger or
automatic self-modification is part of this release.
