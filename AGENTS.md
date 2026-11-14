# SoloOS development rules

Build the authorized SoloOS scope. The user approved completing Phases 2–5 after
the Phase 1 handoff. Keep the existing GitHub repository private with no open-source
license. Updating that repository is authorized; public distribution, hosted service
deployment and live business actions still require their own authorization.

The installable runtime lives entirely in `.agents/skills/soloos/`. Keep tests,
project documentation and development tooling outside it. Preserve user changes.
Use Python 3.11+, Decimal money arithmetic, JSON Schema validation and pytest.
Never substitute missing business evidence with zero or silently combine currencies.
Keep business records separate from executable instructions and credentials.
External writes require explicit scoped authorization and a verified available adapter.
Distinguish implemented, tested, manually reviewed, and planned capabilities.
Run automated tests after behavior changes and update milestone documentation.
Provide a brief user update at each completed unit or stage.
