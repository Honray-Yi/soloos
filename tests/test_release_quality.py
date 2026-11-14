import importlib.util
import json
from pathlib import Path
import threading

import pytest

from soloos.actions import Journal, execute_action, propose
from soloos.data import fingerprint
from soloos.management import department_review
from test_actions import approve, Connector


def test_concurrent_execution_is_not_duplicated(tmp_path):
    action=propose('company','example/repo','Synthetic title','Synthetic body')
    journal=Journal(tmp_path/'journal.sqlite')
    approvals=[approve(journal,action,'external_write'),approve(journal,action,'high_risk')]
    entered,release=threading.Event(),threading.Event()
    class Blocking(Connector):
        def execute(self,action):
            self.calls += 1; entered.set()
            assert release.wait(5)
            return {'number':1}
    connector=Blocking(); results=[]
    def first():
        try: results.append(execute_action(action,journal,connector,*approvals,True))
        except Exception as exc: results.append(exc)
    worker=threading.Thread(target=first); worker.start()
    assert entered.wait(5)
    try:
        with pytest.raises(PermissionError,match='unresolved'):
            execute_action(action,journal,connector,*approvals,True)
    finally:
        release.set(); worker.join(5)
    assert connector.calls==1 and results[0]['status']=='succeeded'


def test_department_findings_are_distinct(business):
    review=department_review(business,'2026-11-02','2026-11-08')
    findings=[json.dumps(v['findings'],sort_keys=True) for v in review['departments'].values()]
    assert len(set(findings))==8


def test_installer_rejects_unreviewed_changes(tmp_path):
    root=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location('installer',root/'tools/install_skill.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    source=tmp_path/'source'; dest=tmp_path/'dest'; base=tmp_path/'baseline'
    for folder in (source,dest,base): folder.mkdir()
    (source/'SKILL.md').write_text('new'); (dest/'SKILL.md').write_text('user edit'); (base/'SKILL.md').write_text('old')
    with pytest.raises(FileExistsError): module.install(source,dest,base)
    assert (dest/'SKILL.md').read_text()=='user edit'
    (dest/'SKILL.md').write_text('old')
    module.install(source,dest,base)
    assert (dest/'SKILL.md').read_text()=='new'
