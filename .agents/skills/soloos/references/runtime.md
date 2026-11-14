# Runtime and capability fallback

Resolve all paths relative to the installed skill folder. Do not rely on a development
checkout. Python 3.11+ and the packages in `scripts/requirements.txt` are required.
Use an existing suitable environment or a local virtual environment. Dependency
installation may need network access; offline operation works once installed.

From the skill root, with a suitable Python interpreter:

```text
python scripts/soloos_cli.py capabilities
python scripts/soloos_cli.py init --demo --out /user/chosen/demo.json
python scripts/soloos_cli.py validate /user/chosen/demo.json
python scripts/soloos_cli.py kpis /user/chosen/demo.json --start 2026-11-02 --end 2026-11-08
python scripts/soloos_cli.py weekly-report /user/chosen/demo.json --start 2026-11-02 --end 2026-11-08 --out /user/chosen/weekly.md
python scripts/soloos_cli.py marketing-budget /user/chosen/demo.json --start 2026-11-02 --end 2026-11-08 --monthly-increase 600.00 --contribution-margin 0.60 --out /user/chosen/decision.json
```

Paths above are illustrative: use actual platform paths. For a real profile use
`init --name NAME --business-type consulting --currency MYR --timezone Asia/Kuala_Lumpur
--start YYYY-MM-DD --end YYYY-MM-DD --out PATH`. It starts with unconfirmed metadata,
incomplete coverage, no cash snapshot and no transactions. Import and verify records;
do not mark evidence confirmed merely because it passes structural validation.
There is no overwrite flag and no execute command. Output defaults to stdout except init.

## ChatGPT and constrained environments

Check actual file access, code execution, dependencies and artifact export separately.
If all are present, use the same portable scripts. If scripts cannot run, request a
dataset or exported CLI results and provide an advisory review. Label manual arithmetic
as unverified, do not claim schema validation or tests ran, and explain how to reproduce
the result locally. If files cannot be saved, return the proposed content for the user
to save. Chat history is not storage. No persistence, connector or scheduling capability
is implied by loading this skill. Live ChatGPT installation is not tested in Phase 1.
