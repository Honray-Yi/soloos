# SoloOS development rules

Build only the phase authorized by the user. Phases 0 and 1 are authorized;
request approval before Phase 2. The user has authorized creating a private GitHub
repository and uploading Phase 1, without an open-source license. Do not make it
public, deploy services, or contact third parties beyond that authorized upload.

The installable runtime lives entirely in `.agents/skills/soloos/`. Keep tests,
project documentation and development tooling outside it. Preserve user changes.
Use Python 3.11+, Decimal money arithmetic, JSON Schema validation and pytest.
Never substitute missing business evidence with zero or silently combine currencies.
Keep business records separate from executable instructions and credentials.
External writes require explicit authorization; Phase 1 has no execution adapter.
Distinguish implemented, tested, manually reviewed, and planned capabilities.
Run automated tests after behavior changes and update milestone documentation.
Provide a brief user update at each completed unit or stage.
