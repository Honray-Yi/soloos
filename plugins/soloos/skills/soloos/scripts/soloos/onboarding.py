"""Create an empty profile or a deterministic fictional business dataset."""

from copy import deepcopy
from datetime import datetime, timezone as utc_timezone

from .data import ROOT, load, validate


def initialize(name, business_type, currency, timezone, minor_units, start, end):
    metadata = {
        "source": "founder onboarding", "recorded_at": datetime.now(utc_timezone.utc).isoformat(),
        "currency": currency, "timezone": timezone, "validation_status": "unverified",
        "evidence": "assumption", "provenance": ["Founder must confirm profile and import records"],
    }
    return validate({
        "schema_version": "1.0",
        "company": {"id": "company-1", "name": name, "business_type": business_type,
                    "minor_units": minor_units, "synthetic": False, "metadata": deepcopy(metadata)},
        "coverage": {"start": start, "end": end, "complete": False, "metadata": deepcopy(metadata)},
        "transactions": [],
    })


def demo():
    return load(ROOT / "assets/demo-business.json")
