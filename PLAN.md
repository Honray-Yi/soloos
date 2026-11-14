# SoloOS delivery plan

## Current completion record
Phases 2–5 were authorized by the user and implemented. The local skill, generated
plugin, private marketplace and ZIP are ready. 149 installed-runtime tests pass;
Codex recognizes the plugin as available. See ROADMAP.md and QA.md for delivered
scope and external acceptance tests not performed. The remaining handoff step is
the private GitHub update and release CI verification. Those release checks subsequently
passed on 2026-11-15; see QA.md. The user's added request for a prompt-only edition and
clear repository navigation is implemented separately without changing runtime authority.

Earlier Phase 1 stop instructions below are historical milestones, superseded by
the user's authorization to complete the project.

## Completion plan — authorized 2026-11-14
1. Phase 2: eight department workflows, six usable business templates, custom KPI
   definitions, and a shared operational record model. Acceptance: template arithmetic,
   evidence gaps, routing and cross-department priorities have regression coverage.
2. Phase 3: all five requested report cadences, bounded scenario forecasts, decision outcome
   evaluation and optional SQLite persistence. Acceptance: calendar boundaries,
   provenance, duplicate records, rollback and missing data are tested.
3. Phase 4: optional real GitHub connector, scoped expiring approvals, durable audit
   journal and duplicate/ambiguous-operation handling. Acceptance: default dry-run,
   changed payloads, absent approval, missing capability and retries fail closed.
   Do not exercise live business writes just to test the connector.
4. Phase 5: current-format skill-only plugin package, portable archive and host
   compatibility guidance. Acceptance: validate manifest/paths, execute unpacked
   runtime, run all tests and GitHub CI, and record any unavailable live host checks.

Use the skill-creator workflow for this substantial skill update. Preserve original
Phase 1 behavior and data compatibility. Stage changes and verify before replacing
protected installed files. Publish the completed source to the existing private repo.

## Phase 0 — conventions and workspace
- Inspect existing work and governing instructions; preserve existing files.
- Review official skill docs, Agent Skills specification and openai/skills.
- Locate Python 3.11+ and test dependencies.
- Acceptance: record sources, architecture boundaries and reproducible commands.

## Phase 1 — functional vertical slice
1. Data contract and onboarding: fictional company initialization, strict schema,
   provenance, evidence classification, currency/timezone and coverage validation.
2. Deterministic analysis: cash-basis revenue, expenses, profit and conditional runway.
3. Management workflow: weekly report and CEO/CFO/CMO marketing budget proposal.
4. Quality and packaging: negative tests, standalone runtime smoke test, skill
   validation, installation instructions and clearly documented limitations.

Acceptance: initialize and validate a fictional dataset; reproduce expected KPIs;
generate a seven-day report and marketing scenario; refuse unauthorized execution;
pass automated tests; run copied skill without development repository imports.

Stop after Phase 1 and request approval for Phase 2. No backend, external connector,
plugin publishing, autonomous scheduling or self-modifying skill in this phase.

## Milestone completion
- Phase 0 complete: sources and discovery conventions recorded in DEPLOYMENT.md;
  empty workspace preserved; Python 3.12 environment configured.
- Phase 1 data and arithmetic complete: schema validation, empty onboarding, synthetic
  fixture and cash-basis metrics verified by automated regressions.
- Phase 1 workflows complete: report and proposed marketing decision generated with
  lineage and fail-closed execution policy.
- Phase 1 quality complete: 90 tests pass from installed runtime; skill validator passes;
  standalone-copy test passes. See QA.md for actual environment and untested surfaces.
- Phase 2 not started. Await explicit user approval per working rule 9.
