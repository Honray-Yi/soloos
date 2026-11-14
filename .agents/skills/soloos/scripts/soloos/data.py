"""Strict input validation and non-overwriting local persistence."""

import hashlib
import json
import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
FORMAT_CHECKER = FormatChecker()


@FORMAT_CHECKER.checks("date-time", raises=(ValueError, TypeError))
def offset_datetime(value):
    """Validate RFC3339 without jsonschema's optional date-time dependency."""
    if not isinstance(value, str):
        return True  # JSON Schema's type keyword handles this.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:[0-5]\d:[0-5]\d(\.\d+)?([Zz]|[+-](?:[01]\d|2[0-3]):[0-5]\d)", value):
        return False
    parsed = datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
    return parsed.utcoffset() is not None


def fingerprint(value):
    """Content identity for traceability; not a signature or execution receipt."""
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def trusted(record):
    meta = record["metadata"]
    return meta["evidence"] == "confirmed" and meta["validation_status"] == "validated"


def validate(data):
    schema = json.loads((ROOT / "assets/business.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    errors = sorted(validator.iter_errors(data), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        raise ValueError(f"Schema error at {'/'.join(map(str, error.path)) or '/'}: {error.message}")
    company = data["company"]
    meta = company["metadata"]
    records = [company, data["coverage"], *data["transactions"], *data.get('entities', []), *data.get('measurements', [])]
    if "cash_snapshot" in data:
        records.append(data["cash_snapshot"])
    for record in records:
        rm = record["metadata"]
        try:
            ZoneInfo(rm["timezone"])
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ValueError(f"Unknown timezone: {rm['timezone']}") from exc
        if rm["currency"] != meta["currency"] or rm["timezone"] != meta["timezone"]:
            raise ValueError("All records must use the company reporting currency and timezone; normalize explicitly first")
        amount = record.get("amount", record.get("available_cash"))
        if amount is not None and -Decimal(amount).as_tuple().exponent > company["minor_units"]:
            raise ValueError("Money precision exceeds company minor_units")
        for field in ('price', 'unit_cost', 'budget', 'value'):
            if field in record and (record.get('record_type') != 'Measurement' or record.get('unit') == 'money'):
                if -Decimal(record[field]).as_tuple().exponent > company['minor_units']:
                    raise ValueError('Money precision exceeds company minor_units')
    coverage = data["coverage"]
    if date.fromisoformat(coverage["start"]) > date.fromisoformat(coverage["end"]):
        raise ValueError("Coverage start must not exceed end")
    ids = set()
    for transaction in data["transactions"]:
        if transaction["id"] in ids:
            raise ValueError(f"Duplicate transaction ID: {transaction['id']}")
        ids.add(transaction["id"])
        if transaction["company_id"] != company["id"]:
            raise ValueError("Transaction belongs to a different company")
    entity_ids = {r['id']: r['record_type'] for r in data.get('entities', [])}
    measurement_keys = set()
    for row in [*data.get('entities', []), *data.get('measurements', [])]:
        if row['id'] in ids:
            raise ValueError('Duplicate record ID: ' + row['id'])
        ids.add(row['id'])
        if row['company_id'] != company['id']:
            raise ValueError('Record belongs to a different company')
        for field, kind in [('goal_id', 'Goal'), ('project_id', 'Project'), ('product_id', 'Product')]:
            if field in row and entity_ids.get(row[field]) != kind:
                raise ValueError('Missing or wrong-type reference: ' + field)
        if row['record_type'] == 'Measurement':
            if row['start'] > row['end']:
                raise ValueError('Measurement start must not exceed end')
            key = (row['metric'], row['start'], row['end'])
            if key in measurement_keys:
                raise ValueError('Duplicate measurement for metric and period')
            measurement_keys.add(key)
            if row['metric'] in ('revenue', 'expenses', 'profit'):
                raise ValueError('Measurement cannot replace a reserved financial KPI')
            value = Decimal(row['value'])
            if row['unit'] in ('count', 'hours') and value < 0:
                raise ValueError('Counts and hours must be nonnegative')
            if row['unit'] == 'count' and value != value.to_integral_value():
                raise ValueError('Counts must be integral')
    custom_names = [r['name'] for r in data.get('custom_kpis', [])]
    if len(set(custom_names)) != len(custom_names):
        raise ValueError('Duplicate custom KPI name')
    return data


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path):
    return validate(json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=_unique_object))


def save_new(path, text):
    """Exclusive creation preserves existing user artifacts, including symlinks."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def local_date(timestamp, timezone):
    return datetime.fromisoformat(timestamp.upper().replace("Z", "+00:00")).astimezone(ZoneInfo(timezone)).date()
