# SoloOS — Solo Founder Operating System

[![SoloOS tests](https://github.com/Honray-Yi/soloos/actions/workflows/tests.yml/badge.svg)](https://github.com/Honray-Yi/soloos/actions/workflows/tests.yml)

**One Founder. One Company. One Intelligent Operating System.**

**只想复制提示词、不安装程序？** 使用 [SoloOS 简易版](prompt-edition/README.md)：
八个角色守则、协作流程和可编辑的个性化设置。完整项目的文件用途见
[仓库导航 / Repository map](REPOSITORY_MAP.md)。

For a no-code, copy-and-paste workflow, use the separate [prompt-only edition](prompt-edition/README.md).
It provides editable role prompts; it does not inherit the runtime's programmatic validation or execution controls.

SoloOS 1.0 is a local-first management skill for solo founders. It combines validated
business data, deterministic calculations, management reporting and explicitly
authorized operations. No mandatory paid API, server or hosted database.

## What works
- Eight department reviews: CEO, CFO, CMO, Sales, COO, CTO/Product, HR/Partnership, BI.
- Six KPI templates: SaaS, e-commerce, creator, freelance, consulting, digital products;
  custom businesses can define safe arithmetic metrics.
- Company onboarding and a unified model for Company, Goal, Project, Task,
  Transaction, Customer, Product, Campaign, Decision and Report.
- Cash-basis revenue, expenses, profit and conditional runway; confirmed facts remain
  distinct from assumptions, estimates and forecasts.
- Daily, weekly, monthly, quarterly and annual reports; explicit cash scenarios.
- Immutable JSON/SQLite snapshots, decision logs and outcome evaluation.
- Proposal-first GitHub issue creation with separate scoped approvals, expiry,
  duplicate suppression and a durable execution journal.

Other business writes (payments, contracts, deletion, advertising changes and binding
communications) are not implemented connectors and remain proposals. No scheduler
or autonomous self-modification is included.

## Start with the skill
Clone this private repository using your authenticated GitHub account. Open Codex in
the repository and invoke `$soloos`. Install Python dependencies before asking it to
run calculations. The portable runtime is [.agents/skills/soloos](.agents/skills/soloos).
Copy that entire folder into another project's `.agents/skills/` for repo-scoped use.

Example:
> Use $soloos to review this week's business data, identify the strongest constraint,
> and assess a marketing budget increase. Show evidence gaps and propose next actions.

## Quick start
Requires Python 3.11+. From the repository root on Windows PowerShell:

```powershell
py -3.11 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .agents/skills/soloos/scripts/requirements.txt
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py init --demo --out work/demo.json
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py validate work/demo.json
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py report examples/management-business.json --cadence weekly --anchor 2026-11-04 --out work/report.md
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py review examples/management-business.json --start 2026-11-02 --end 2026-11-08 --out work/review.json
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py forecast examples/management-business.json --start 2026-11-02 --end 2026-11-08 --months 3
```

Use your installed 3.11+ interpreter if different. On macOS/Linux use
`python3 -m venv .venv`, then `.venv/bin/python`. Existing output files are never
overwritten. `--help` documents every command; `--format json` exports report records.

The fictional demo has MYR 2,000 revenue, 2,700 expenses, -700 cash-basis profit,
and 4.00 months estimated runway. The extended consulting fixture has a 60% project
contribution margin and 60% utilization. These are synthetic examples, not benchmarks.

## Plugin distribution
The same runtime is packaged under [plugins/soloos](plugins/soloos), with a current
Agent Plugins manifest and a private repo marketplace. It includes no server or
credential. See [DEPLOYMENT.md](DEPLOYMENT.md) for host-specific installation.

```text
python tools/build_plugin.py --output work/new-plugin --archive dist/soloos-plugin.zip
```

The builder requires fresh output paths and writes SHA-256 checksums. The committed
distribution is checked against the canonical runtime to prevent drift. Do not edit
generated copies independently. Choose the standalone skill or installed plugin
for a project to avoid duplicate skill entries.

## Execution requires human review
All normal analysis is read-only; requested local exports and storage are explicit.
GitHub writes need a token supplied outside the repository, an exact action proposal,
two human approval steps, unexpired scoped approvals and `--execute`. Dry-run is the
default. Read [the operations guide](.agents/skills/soloos/references/operations.md)
before using it. A network timeout blocks automatic retry and requires reconciliation.
The local journal is not a tamper-proof identity service or an exactly-once guarantee
from GitHub. No live business write was performed merely to test this release.

## Tests and examples
```text
python -m pip install -r requirements-dev.txt
python -m pytest
```

Use your virtual environment's Python. Tests cover business arithmetic, schema and
relationship validation, missing evidence, report periods, storage, approvals, duplicate
and concurrent operations, HTTP contracts, and extracted-package execution.

- [Executive report](examples/executive-report-v1.md)
- [Eight-department review](examples/management-review.json)
- [Cash scenario](examples/cash-forecast.json)
- [Decision outcome](examples/decision-outcome.json)
- [QA evidence and compatibility limits](QA.md)

## Repository structure
```text
.agents/skills/soloos/   Canonical standalone runtime
prompt-edition/         Standalone, editable text prompts (Chinese default)
.agents/plugins/        Local marketplace catalog
plugins/soloos/         Generated portable plugin
packaging/              Manifest, catalog and official schema sources
tests/                  Deterministic, regression and negative tests
examples/               Fictional datasets and generated results
tools/                  Development and packaging helpers
```

See [PRD](PRD.md), [architecture](ARCHITECTURE.md), [roadmap](ROADMAP.md),
[contributing](CONTRIBUTING.md), [security](SECURITY.md) and [changelog](CHANGELOG.md).

Release verification: **150 automated tests passed locally**, and all six Windows/Linux
and Python 3.11–3.13 jobs passed for the corrected v1 package.
[Verified CI run](https://github.com/Honray-Yi/soloos/actions/runs/43614128409).
Documentation link checks also run in CI; prompt quality review is not a claim of
behavioral testing on every AI model.

This repository remains **private with no open-source license**. No redistribution
or sublicensing permission is granted by this README. Dependencies and the attributed
plugin specification retain their own terms. Live ChatGPT installation and production
connector acceptance are not implied by local tests or Codex discovery.
