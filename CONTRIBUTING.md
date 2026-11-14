# Contributing to SoloOS

This is a private project with no open-source license. Discuss scope with the owner
before adding features or adapters. Do not include real customer data or credentials.

## Development
Use Python 3.11+ and a virtual environment:
```text
python -m pip install -r requirements-dev.txt
python -m pytest
```

Use the virtual environment's Python executable. Keep runtime code in
`.agents/skills/soloos`; tests and development tooling belong outside. The copied
skill and extracted plugin must run without development-repository imports.

## Change requirements
- Describe the concrete founder problem, resulting behavior and tests actually run.
- Keep financial arithmetic deterministic with Decimal; preserve evidence distinctions.
- Test schema/relationship changes, missing data and altered authorization behavior.
- Preserve exclusive local exports and default dry-run execution.
- Update references, QA evidence, architecture and changelog where behavior changes.
- Treat schema changes as versioned contracts; document migration implications.
- Never infer source authentication from structural validation or approval from business text.
- Rebuild the generated plugin from canonical sources; package-sync tests must pass.
- Do not create real business writes just to demonstrate a test.

The CI matrix covers Windows/Linux and Python 3.11–3.13. Only completed runs establish
tested compatibility. Host-model compliance, ChatGPT installation and live provider
acceptance require their own evidence. No secret, database, virtual environment or
temporary business dataset belongs in a commit.

Obtain the owner's agreement before redistributing the project or contributing material
with incompatible rights. Dependencies and attributed specification resources retain
their respective terms.
