"""Scoped approvals and a durable fail-closed execution journal.

The local OS user owns the journal. This is not an adversarial multi-user identity
system; a process with direct DB write access is inside the trust boundary.
"""
from contextlib import closing
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import re
import sqlite3
import uuid

from jsonschema import Draft202012Validator

from .data import ROOT, fingerprint, FORMAT_CHECKER


def now(): return datetime.now(timezone.utc)


def validate_action(action):
    schema = json.loads((ROOT/'assets/action.schema.json').read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema,format_checker=FORMAT_CHECKER).iter_errors(action))
    if errors: raise ValueError('Invalid action: ' + errors[0].message)
    if action['kind'] == 'github.create_issue' and not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', action['target']):
        raise ValueError('GitHub target must be owner/repository')
    return action


def propose(company_id, target, title, body, kind='github.create_issue', idempotency_key=None):
    action = {'schema_version':'1.0', 'company_id':company_id, 'kind':kind, 'target':target,
              'payload':{'title':title,'body':body}, 'risk':'high',
              'idempotency_key':idempotency_key or uuid.uuid4().hex,
              'metadata': {'source':'founder action proposal','recorded_at':now().isoformat(),
                           'currency':'XXX','timezone':'UTC','validation_status':'unverified','evidence':'assumption',
                           'provenance':['User-supplied nonmonetary action; XXX means no currency applies']}}
    return validate_action(action)


class Journal:
    def __init__(self, path): self.path = Path(path)

    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        con.execute('PRAGMA synchronous=FULL')
        con.executescript('''
          CREATE TABLE IF NOT EXISTS operations (key TEXT PRIMARY KEY, digest TEXT NOT NULL, state TEXT NOT NULL, result TEXT);
          CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, digest TEXT NOT NULL, scope TEXT NOT NULL, actor TEXT NOT NULL, expires TEXT NOT NULL, consumed INTEGER NOT NULL DEFAULT 0);
          CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, event TEXT NOT NULL, digest TEXT NOT NULL, detail TEXT NOT NULL);
        ''')
        return con

    @staticmethod
    def event(con, event, digest, detail):
        con.execute('INSERT INTO audit(at,event,digest,detail) VALUES (?,?,?,?)',
                    (now().isoformat(),event,digest,json.dumps(detail,sort_keys=True)))

    def approve(self, action, actor, scope, confirmation, minutes=15):
        validate_action(action)
        digest = fingerprint(action)
        if scope not in ('external_write','high_risk') or not actor.strip():
            raise ValueError('An identified actor and explicit approval scope are required')
        if confirmation != f'APPROVE {scope} {digest}':
            raise PermissionError('Exact action fingerprint and approval scope must be acknowledged')
        if type(minutes) is not int or not 1 <= minutes <= 60:
            raise ValueError('Approval lifetime must be 1 to 60 minutes')
        token = uuid.uuid4().hex
        with closing(self.connect()) as con:
            con.execute('BEGIN IMMEDIATE')
            try:
                con.execute('INSERT INTO approvals(id,digest,scope,actor,expires) VALUES (?,?,?,?,?)',
                            (token,digest,scope,actor,(now()+timedelta(minutes=minutes)).isoformat()))
                self.event(con,'approval_granted',digest,{'approval_id':token,'scope':scope,'actor':actor})
                con.commit()
            except Exception:
                con.rollback(); raise
        return token

    def events(self):
        if not self.path.exists(): return []
        with closing(sqlite3.connect(self.path.resolve().as_uri()+'?mode=ro',uri=True)) as con:
            return [dict(zip(('seq','at','event','digest','detail'),row)) for row in con.execute('SELECT seq,at,event,digest,detail FROM audit ORDER BY seq')]


def execute_action(action, journal, connector=None, approval_id=None, high_risk_approval_id=None, execute=False):
    validate_action(action)
    digest = fingerprint(action)
    if not execute:
        return {'status':'proposed','action_digest':digest,'action':action,'executed':False}
    with closing(journal.connect()) as con:
        con.execute('BEGIN IMMEDIATE')
        try:
            previous = con.execute('SELECT digest,state,result FROM operations WHERE key=?',(action['idempotency_key'],)).fetchone()
            if previous:
                if previous[0] != digest: raise PermissionError('Idempotency key is already bound to different content')
                if previous[1] == 'succeeded':
                    journal.event(con,'duplicate_suppressed',digest,{})
                    con.commit()
                    return {'status':'succeeded','replayed':True,'result':json.loads(previous[2])}
                raise PermissionError('Previous operation is unresolved; reconcile externally before any new action. No automatic retry.')
            if connector is None or not connector.supports(action['kind']):
                raise PermissionError('No capable connector; retain the proposal')
            if not connector.available(): raise PermissionError('Connector credentials/capability are unavailable')
            for token, scope in [(approval_id,'external_write'),(high_risk_approval_id,'high_risk')]:
                row = con.execute('SELECT digest,scope,expires,consumed FROM approvals WHERE id=?',(token,)).fetchone()
                if not row or row[0] != digest or row[1] != scope or row[3]:
                    raise PermissionError('Missing, mismatched or consumed ' + scope + ' approval')
                expiry = datetime.fromisoformat(row[2])
                if expiry.tzinfo is None or expiry <= now(): raise PermissionError('Approval expired')
            con.execute('INSERT INTO operations(key,digest,state) VALUES (?,?,?)',(action['idempotency_key'],digest,'in_flight'))
            con.execute('UPDATE approvals SET consumed=1 WHERE id IN (?,?)',(approval_id,high_risk_approval_id))
            journal.event(con,'execution_started',digest,{'kind':action['kind'],'target':action['target']})
            con.commit()  # Durable before making an external request.
        except Exception as exc:
            con.rollback()
            journal.event(con,'execution_denied',digest,{'reason':str(exc)})
            raise
    try:
        result = connector.execute(action)
        if not isinstance(result, dict): raise ValueError('Invalid connector response')
        encoded = json.dumps(result, allow_nan=False)
    except Exception as exc:
        # An HTTP failure or timeout can occur after the server accepted a write.
        # Do not record raw exception text: it can contain tokens or request data.
        with closing(journal.connect()) as con:
            con.execute('BEGIN IMMEDIATE')
            con.execute('UPDATE operations SET state=? WHERE key=?',('unknown',action['idempotency_key']))
            journal.event(con,'execution_unknown',digest,{'error_type':type(exc).__name__})
            con.commit()
        raise RuntimeError('External outcome is unknown; inspect the provider and audit journal. Do not retry automatically.') from None
    with closing(journal.connect()) as con:
        con.execute('BEGIN IMMEDIATE')
        con.execute('UPDATE operations SET state=?,result=? WHERE key=?',('succeeded',encoded,action['idempotency_key']))
        journal.event(con,'execution_succeeded',digest,{'result':result})
        con.commit()
    return {'status':'succeeded','replayed':False,'result':result}
