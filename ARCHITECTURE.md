# SoloOS architecture

## Boundaries
The development repository contains tests, quality tooling and product documentation.
The portable runtime is `.agents/skills/soloos/`, containing SKILL.md, metadata,
references, Python modules and schema/sample assets. It imports nothing from the
repository root and uses no API or database. `work/` is disposable local development
staging/output; it is ignored by Git and is not the distribution source.

Flow: host capability check -> intent routing -> validated local JSON -> deterministic
financial functions -> Report/Decision record -> optional user-requested local export.
Natural-language interpretation belongs to the host model; exact-label CLI routing
does not pretend to be an NLP engine. Business data never grants tool authorization.

## Modules
- `data`: Draft 2020-12 validation, semantic checks, fingerprints, exclusive file writes.
- `onboarding`: empty profile or fixed synthetic fixture.
- `finance`: Decimal cash-basis totals and conditional runway.
- `reporting`: seven-day report, explicit completeness and Markdown rendering.
- `decisions`: bounded monthly-spend scenario and CEO/CFO/CMO prompts.
- `records`: schema-validated output envelope and evidence lineage.
- `permissions`: fail-closed execution stub; always denies, including with approval.
- `routing`, `cli`: explicit command surface and capability disclosure.

## Unified model and staged coverage
All records share identity, company linkage and metadata: source, timestamp, currency,
timezone, validation status, evidence class and provenance. Company establishes reporting
settings. Decimal strings avoid binary floating-point loss. `minor_units` must be
verified by the importer; currency codes are syntactically validated, not an ISO registry.

| Record | Phase 1 | Intended later relationships |
| --- | --- | --- |
| Company | Validated profile | Parent of all records |
| Transaction | Validated settled cash movements | Customer/Product/Campaign attribution |
| Report | Generated weekly record | Period and input snapshot lineage |
| Decision | Generated proposal | Goal, actions and measured outcome |
| Goal | Planned | Company objective, target and measurement window |
| Project | Planned | Company/Goal, owner, status |
| Task | Planned | Project, owner, due date |
| Customer | Planned | Company, source identity and consent scope |
| Product | Planned | Company, price and delivery economics |
| Campaign | Planned | Product, channel, spend and attribution |

Coverage and cash snapshot are auxiliary records with the same evidence metadata.
Schema validation is not evidence authentication. Reconciliation remains a founder task.
Output payload validation checks required Phase 1 structure; it is not a generic
business object store. Future schema versions require explicit migrations.

## Safety and persistence
The CLI has no network or external-write adapter and no execute command. The Python
execution boundary always raises PermissionError. Approvals are not implemented as
trusted credentials. Future connectors must independently verify scoped authorization,
separate high-risk approvals, use idempotency keys and append durable execution audits.
Content hashes only identify local proposals; they are not security signatures.

JSON files are durable only when saved. The caller chooses storage and backups. SQLite
is an optional future adapter behind these records, not an MVP dependency. Do not use
conversation history as a record database. No secrets belong in fixtures or source.

## Tradeoffs and limits
Phase 1 deliberately uses cash-basis management figures and a constant-rate runway
scenario. No accrual accounting, FX conversion, bank reconciliation or market-response
forecast is implied. Local Python behavior is automated-tested; model compliance and
ChatGPT installation need separate host evaluations before distribution claims.
