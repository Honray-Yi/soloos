from copy import deepcopy
import json

import pytest
from soloos.data import load, validate, save_new
from soloos.onboarding import initialize


@pytest.mark.parametrize("field,value", [("amount", "-1"), ("amount", "NaN"), ("amount", 0.1),
    ("amount", "0.001"), ("occurred_at", "2026-11-31T10:00:00Z"),
    ("occurred_at", "2026-11-01T10:00:00"), ("company_id", "someone-else"), ("kind", "unknown")])
def test_rejects_bad_transactions(business, field, value):
    business["transactions"][0][field] = value
    with pytest.raises(ValueError):
        validate(business)


@pytest.mark.parametrize("field,value", [("currency", "USD"), ("timezone", "Mars/Base"), ("provenance", []), ("evidence", "probably")])
def test_rejects_bad_metadata(business, field, value):
    business["transactions"][0]["metadata"][field] = value
    with pytest.raises(ValueError):
        validate(business)


def test_duplicate_ids(business):
    business["transactions"].append(deepcopy(business["transactions"][0]))
    with pytest.raises(ValueError, match="Duplicate"):
        validate(business)


def test_unknown_fields_rejected(business):
    business["credential"] = "not-a-real-secret"
    with pytest.raises(ValueError):
        validate(business)


def test_duplicate_json_keys_rejected(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"company": 1, "company": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate JSON key"):
        load(path)


def test_initialization_has_unknown_actuals():
    data = initialize("Test", "consulting", "MYR", "Asia/Kuala_Lumpur", 2, "2026-11-02", "2026-11-08")
    assert not data["coverage"]["complete"] and "cash_snapshot" not in data
    assert data["company"]["metadata"]["evidence"] == "assumption"


def test_save_preserves_existing_work(tmp_path):
    path = tmp_path / "user.json"
    save_new(path, "original")
    with pytest.raises(FileExistsError):
        save_new(path, "replacement")
    assert path.read_text() == "original"
