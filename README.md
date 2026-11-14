# SoloOS — Solo Founder Operating System

**One Founder. One Company. One Intelligent Operating System.**

Phase 1 local preview: turn validated business records into cash-basis KPIs, a weekly
executive report and a CEO/CFO/CMO marketing budget proposal. No paid API or backend.
This is a working vertical slice, not the complete eight-department product.

## Use as a Codex skill
Clone this private repository using your authenticated GitHub account, open Codex in
the repository, and invoke `$soloos`. The skill is discovered from
`.agents/skills/soloos/SKILL.md`. Install the Python dependencies below before asking
it to run calculations. See [deployment and ChatGPT compatibility](DEPLOYMENT.md)
for copying the skill into another project and the limits of other host environments.

Example request:

> Use $soloos to review my weekly business data, identify evidence gaps, and assess
> a proposed monthly marketing increase. Produce a proposal without executing changes.

## Repository layout
```text
.agents/skills/soloos/   Portable skill: instructions, metadata, scripts, schemas, fixture
.github/                Automated CI and issue/pull-request templates
examples/               Generated fictional report and decision
tests/                  Deterministic, regression and negative tests
tools/                  Development helpers; not needed by the installed skill
```

## Implemented and planned
| Capability | Status |
| --- | --- |
| Company onboarding and JSON validation | Implemented and locally tested |
| Cash-basis KPIs and weekly reports | Implemented and locally tested |
| CEO/CFO/CMO marketing budget review | Implemented and locally tested |
| External writes | Disabled in Phase 1 |
| Eight departments and six templates | Planned, not implemented |
| Plugin distribution and live ChatGPT acceptance | Planned, not verified |

## Quick start
Requires Python 3.11+. From the repository root, on Windows PowerShell:

```powershell
py -3.11 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .agents/skills/soloos/scripts/requirements.txt
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py init --demo --out work/demo.json
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py validate work/demo.json
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py kpis work/demo.json --start 2026-11-02 --end 2026-11-08
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py weekly-report work/demo.json --start 2026-11-02 --end 2026-11-08 --out work/weekly.md
& .\.venv\Scripts\python.exe .agents/skills/soloos/scripts/soloos_cli.py marketing-budget work/demo.json --start 2026-11-02 --end 2026-11-08 --monthly-increase 600.00 --contribution-margin 0.60 --out work/decision.json
```

Use your installed 3.11+ interpreter instead of `py -3.11` if needed. On macOS/Linux,
create the environment with `python3 -m venv .venv` and use `.venv/bin/python` for each
command. Paths under the skill stay identical. Output paths must be new; existing
files are never overwritten. JSON reports are available with `--format json`.

Expected demo: MYR 2,000 revenue, 2,700 expenses, -700 cash-basis profit, 4.00 months
estimated runway. A MYR 600 recurring monthly marketing increase gives 3.33 months
downside runway and requires MYR 1,000 extra monthly revenue at an **assumed** 60%
contribution margin. This is fictional scenario arithmetic, not business advice
derived from a real company or a prediction of campaign performance.

## Tests
```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
& .\.venv\Scripts\python.exe -m pytest
```

The portable skill is [.agents/skills/soloos/SKILL.md](.agents/skills/soloos/SKILL.md).
See [PRD](PRD.md), [architecture](ARCHITECTURE.md), [deployment](DEPLOYMENT.md),
[roadmap](ROADMAP.md) and [QA](QA.md) for scope, evidence and limitations.

External writes are unavailable in Phase 1, even with approval. Live ChatGPT installation,
plugin publishing, SQLite, other report cadences and six business templates are planned.
Development stops for user approval before Phase 2. No autonomous self-modification.

Verified locally: **90 tests passed**, valid skill metadata, and standalone copied-skill
execution. Inspect the generated [weekly report](examples/weekly-report.md) and
[marketing proposal](examples/marketing-decision.json). The GitHub Actions matrix is
configured but has not run remotely. See QA.md for the exact verification environment.

## Contributions, security and licensing
Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a change and
[SECURITY.md](SECURITY.md) before reporting security issues. Use only synthetic or
redacted data in issues and tests. This repository is private and has **no open-source
license**; no permission to redistribute or sublicense is granted by this README.
The owner may choose a license later. Dependencies retain their respective licenses.
