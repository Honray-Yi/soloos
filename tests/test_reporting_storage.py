from copy import deepcopy
import json
import sqlite3
import pytest

from soloos.periods import period
from soloos.reporting import executive_report
from soloos.forecast import cash_forecast
from soloos.decisions import marketing_budget
from soloos.outcomes import evaluate
from soloos.storage import Store
from soloos.cli import main
from test_management import measurement


@pytest.mark.parametrize('cadence,anchor,expected', [
    ('daily','2024-02-29',('2024-02-29','2024-02-29')),
    ('weekly','2026-01-01',('2025-12-29','2026-01-04')),
    ('monthly','2024-02-10',('2024-02-01','2024-02-29')),
    ('quarterly','2026-11-14',('2026-10-01','2026-12-31')),
    ('annual','2024-02-29',('2024-01-01','2024-12-31')),
])
def test_periods(cadence, anchor, expected): assert period(cadence, anchor) == expected


def test_full_period_report_withholds_partial_month(business):
    report = executive_report(business, 'monthly', '2026-11-04')
    assert report['payload']['kpis']['revenue'] is None
    assert report['payload']['cadence'] == 'monthly'


def test_forecast_arithmetic_and_lineage(business):
    result = cash_forecast(business,'2026-11-02','2026-11-08',3)
    assert [r['closing_cash'] for r in result['payload']['months']] == ['9000.00','6000.00','3000.00']
    assert result['metadata']['evidence'] == 'forecast'
    business['coverage']['complete'] = False
    assert cash_forecast(business,'2026-11-02','2026-11-08')['payload']['status'] == 'unavailable'


@pytest.mark.parametrize('growth', ['NaN','Infinity','-1.1','1.1','bad'])
def test_invalid_forecast_growth(business, growth):
    with pytest.raises(ValueError): cash_forecast(business,'2026-11-02','2026-11-08',3,growth)


def test_sqlite_roundtrip_dedup_and_read_only(tmp_path, business):
    path = tmp_path/'company.sqlite'
    store = Store(path)
    with pytest.raises(sqlite3.Error): store.history()
    assert not path.exists()
    digest = store.put(business)
    assert store.put(deepcopy(business)) == digest and len(store.history()) == 1
    assert store.get(digest) == business
    report = executive_report(business,'weekly','2026-11-04')
    store.put(report)
    assert len(store.history(business['company']['id'])) == 2
    assert store.history('not-this-company') == []


def test_sqlite_detects_tampering(tmp_path, business):
    path = tmp_path/'db.sqlite'
    store = Store(path)
    digest = store.put(business)
    with sqlite3.connect(path) as con:
        con.execute('UPDATE snapshots SET body=?', ('{}',))
    with pytest.raises(ValueError, match='integrity'): store.get(digest)


def test_outcome_uses_actual_measurement_and_preserves_decision(business, tmp_path):
    decision = marketing_budget(business,'2026-11-02','2026-11-08','600','0.6')
    before = deepcopy(decision)
    business['measurements'] = [measurement(business,'incremental_revenue','1200','money')]
    outcome = evaluate(decision,business,'incremental_revenue','2026-11-02','2026-11-08','1000')
    assert outcome['payload']['assessment'] == 'met' and decision == before
    assert Store(tmp_path/'log.sqlite').put(outcome)
    business['measurements'][0]['metadata']['evidence'] = 'forecast'
    assert evaluate(decision,business,'incremental_revenue','2026-11-02','2026-11-08','1000')['payload']['assessment'] == 'insufficient_evidence'


def test_extended_cli(tmp_path, business, capsys):
    path = tmp_path/'data.json'
    path.write_text(json.dumps(business),encoding='utf-8')
    assert main(['template','saas']) == 0
    assert main(['review',str(path),'--start','2026-11-02','--end','2026-11-08','--department','Sales']) == 0
    assert main(['report',str(path),'--cadence','monthly','--anchor','2026-11-04','--format','json']) == 0
    assert main(['store-put',str(path),'--db',str(tmp_path/'store.sqlite')]) == 0
