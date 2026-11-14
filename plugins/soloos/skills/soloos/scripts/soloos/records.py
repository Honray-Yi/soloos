"""Provenance envelopes for generated Report and Decision records."""

from copy import deepcopy
from datetime import datetime, timezone
import json

from jsonschema import Draft202012Validator

from .data import ROOT, FORMAT_CHECKER, fingerprint
from . import __version__


def record(kind, data, payload, evidence, recorded_at=None):
    meta = deepcopy(data["company"]["metadata"])
    meta.update({"source": "soloos/" + __version__, "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat(),
                 "validation_status": "validated", "evidence": evidence,
                 "provenance": ["dataset:sha256:" + fingerprint(data)]})
    result = {"schema_version": "1.0", "id": kind.lower() + "-" + fingerprint({"data": data, "payload": payload}),
              "record_type": kind, "company_id": data["company"]["id"],
              "synthetic": data["company"]["synthetic"], "metadata": meta, "payload": payload}
    validate_record(result)
    return result


def validate_record(value):
    schema = json.loads((ROOT / "assets/output.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FORMAT_CHECKER).validate(value)
