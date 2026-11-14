# SoloOS delivery plan

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
