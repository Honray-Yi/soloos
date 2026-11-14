# Contributing to SoloOS

This private project is a Phase 1 preview. Discuss scope with the owner before
implementing later phases. Suggestions and bug reports are welcome; do not include
real customer records, credentials or confidential business data.

## Development
Use Python 3.11+ and a virtual environment. From the repository root:

```text
python -m pip install -r requirements-dev.txt
python -m pytest
```

Use the virtual environment's Python executable on your platform. Keep runtime
changes inside `.agents/skills/soloos/`; tests and development helpers belong outside.
The copied skill must run without importing the repository's development files.
Never commit `.venv`, `work`, database files, secrets or user business datasets.

## Change requirements
- Describe the problem, observable behavior and relevant verification.
- Keep money calculations deterministic and use Decimal, not floating-point totals.
- Add regression tests for changed behavior, especially evidence and permissions.
- Update the appropriate reference, README/QA and CHANGELOG when behavior changes.
- Preserve no-overwrite exports and fail-closed external execution in Phase 1.
- Do not treat schema validity as verification of business facts.
- Do not silently change the data contract; document version and migration implications.

Run tests before a pull request. CI covers Windows/Linux and Python 3.11–3.13;
only actual completed runs establish compatibility. A green suite does not establish
host-model compliance or live ChatGPT support.

No open-source license has been granted. Obtain the owner's agreement before
redistributing this project or contributing material with incompatible rights.
