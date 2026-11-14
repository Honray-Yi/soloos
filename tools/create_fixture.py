"""Regenerate the fictional dataset at a new path, never overwrite user data."""

import argparse
from copy import deepcopy
import json
from pathlib import Path


def fixture():
    meta = {"source": "SoloOS synthetic fixture", "recorded_at": "2026-11-09T00:00:00+08:00",
            "currency": "MYR", "timezone": "Asia/Kuala_Lumpur", "validation_status": "validated",
            "evidence": "confirmed", "provenance": ["Fictional values for automated tests; not real business evidence"]}
    company = {"id": "demo-solo", "name": "Lumen Studio (fictional)", "business_type": "consulting",
               "minor_units": 2, "synthetic": True, "metadata": deepcopy(meta)}
    transactions = []
    for identifier, kind, amount, category in [
        ("sale-1", "revenue", "2000.00", "consulting"),
        ("cost-1", "expense", "2200.00", "delivery"),
        ("cost-2", "expense", "500.00", "marketing"),
        ("capital-1", "financing_in", "500.00", "owner_contribution"),
    ]:
        transactions.append({"id": identifier, "company_id": company["id"],
                             "occurred_at": "2026-11-04T12:00:00+08:00", "kind": kind,
                             "amount": amount, "category": category, "metadata": deepcopy(meta)})
    return {"schema_version": "0.1", "company": company,
            "coverage": {"start": "2026-11-02", "end": "2026-11-08", "complete": True, "metadata": deepcopy(meta)},
            "cash_snapshot": {"as_of": "2026-11-08", "available_cash": "12000.00", "metadata": deepcopy(meta)},
            "transactions": transactions}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(fixture(), stream, indent=2)
        stream.write("\n")
