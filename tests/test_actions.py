from copy import deepcopy
from datetime import datetime, timezone, timedelta
import io
import json
import sqlite3

import pytest

from soloos.actions import Journal, propose, execute_action
from soloos.connectors import GitHubIssues, NoRedirect
from soloos.data import fingerprint
from soloos.cli import main


class Connector:
    def __init__(self, fail=False): self.calls=0; self.fail=fail
    def supports(self,kind): return kind == 'github.create_issue'
    def available(self): return True
    def execute(self,action):
        self.calls += 1
        if self.fail: raise TimeoutError('sensitive-token-must-not-be-logged')
        return {'number':7,'url':'https://github.com/example/repo/issues/7'}


@pytest.fixture
def action(): return propose('demo','example/repo','Synthetic task','Synthetic body')


def approve(journal,action,scope):
    return journal.approve(action,'founder',scope,'APPROVE '+scope+' '+fingerprint(action))


def test_dry_run_never_opens_journal_or_connector(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    assert execute_action(action,journal,connector)['status'] == 'proposed'
    assert not journal.path.exists() and connector.calls == 0


def test_missing_approval_fails_closed_and_audits(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    with pytest.raises(PermissionError): execute_action(action,journal,connector,execute=True)
    assert connector.calls == 0 and journal.events()[-1]['event'] == 'execution_denied'


def test_separate_high_risk_approval_required(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    approval = approve(journal,action,'external_write')
    with pytest.raises(PermissionError): execute_action(action,journal,connector,approval,approval,True)
    high = approve(journal,action,'high_risk')
    result = execute_action(action,journal,connector,approval,high,True)
    assert result['status'] == 'succeeded' and connector.calls == 1
    replay = execute_action(action,journal,connector,approval,high,True)
    assert replay['replayed'] and connector.calls == 1


@pytest.mark.parametrize('field', ['target','payload','company_id','idempotency_key'])
def test_approval_cannot_authorize_changed_action(tmp_path,action,field):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    approval, high = approve(journal,action,'external_write'), approve(journal,action,'high_risk')
    changed=deepcopy(action)
    changed[field] = {'title':'changed','body':'new'} if field == 'payload' else ('other/repo' if field == 'target' else 'changed-value')
    with pytest.raises(PermissionError): execute_action(changed,journal,connector,approval,high,True)
    assert connector.calls == 0


def test_expired_approval_rejected(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    approval, high = approve(journal,action,'external_write'), approve(journal,action,'high_risk')
    with sqlite3.connect(journal.path) as con:
        con.execute('UPDATE approvals SET expires=?',(datetime(2020,1,1,tzinfo=timezone.utc).isoformat(),))
    with pytest.raises(PermissionError,match='expired'): execute_action(action,journal,connector,approval,high,True)
    assert connector.calls == 0


def test_unknown_outcome_blocks_retry_and_redacts_error(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector(fail=True)
    approval, high = approve(journal,action,'external_write'), approve(journal,action,'high_risk')
    with pytest.raises(RuntimeError,match='unknown'): execute_action(action,journal,connector,approval,high,True)
    with pytest.raises(PermissionError,match='unresolved'): execute_action(action,journal,connector,approval,high,True)
    assert connector.calls == 1
    assert 'sensitive-token' not in json.dumps(journal.events())


def test_idempotency_key_cannot_be_reused_for_other_payload(tmp_path,action):
    journal, connector = Journal(tmp_path/'journal.sqlite'), Connector()
    execute_action(action,journal,connector,approve(journal,action,'external_write'),approve(journal,action,'high_risk'),True)
    action['payload']['title']='Different'
    with pytest.raises(PermissionError,match='different content'): execute_action(action,journal,connector,execute=True)
    assert connector.calls == 1


@pytest.mark.parametrize('kind',['payment','contract','delete','public_post','binding_communication'])
def test_unsupported_high_risk_operations_remain_proposals(tmp_path,action,kind):
    action['kind']=kind
    with pytest.raises(PermissionError,match='connector'):
        execute_action(action,Journal(tmp_path/'journal.sqlite'),Connector(),execute=True)


def test_approval_requires_exact_confirmation(tmp_path,action):
    with pytest.raises(PermissionError): Journal(tmp_path/'journal.sqlite').approve(action,'founder','external_write','yes')


def test_noninteractive_cli_cannot_issue_approval(tmp_path,action,monkeypatch,capsys):
    file=tmp_path/'action.json'; file.write_text(json.dumps(action),encoding='utf-8')
    monkeypatch.setattr('sys.stdin',io.StringIO('yes'))
    assert main(['action-approve',str(file),'--journal',str(tmp_path/'j.sqlite'),'--actor','founder','--scope','external_write']) == 2
    assert 'interactive human terminal' in capsys.readouterr().err


def test_real_adapter_http_contract_without_network(monkeypatch,action):
    monkeypatch.setenv('SOLOOS_GITHUB_TOKEN','synthetic-test-value')
    captured=[]
    class Response:
        status=201
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def read(self,limit): return b'{"number": 42}'
    class Opener:
        def open(self,request,timeout): captured.append(request); return Response()
    result=GitHubIssues(Opener()).execute(action)
    assert result['number'] == 42
    assert captured[0].full_url == 'https://api.github.com/repos/example/repo/issues'
    assert captured[0].method == 'POST' and action['idempotency_key'] in captured[0].data.decode()


def test_missing_credentials_and_redirect_refusal(monkeypatch):
    monkeypatch.delenv('SOLOOS_GITHUB_TOKEN',raising=False)
    assert not GitHubIssues().available()
    with pytest.raises(RuntimeError): NoRedirect().redirect_request(None,None,302,None,None,'https://untrusted.invalid')
