"""Optional SQLite immutable snapshots and decision log; no model-memory reliance."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from datetime import datetime, timezone

from .data import validate, fingerprint
from .records import validate_record


class Store:
    def __init__(self, path):
        self.path = Path(path)

    def _connect(self, write=False):
        if write:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(self.path, timeout=10)
            con.execute('CREATE TABLE IF NOT EXISTS snapshots (digest TEXT PRIMARY KEY, kind TEXT NOT NULL, company_id TEXT NOT NULL, created_at TEXT NOT NULL, body TEXT NOT NULL)')
        else:
            # Read-only URI cannot accidentally create an empty database.
            con = sqlite3.connect(self.path.resolve().as_uri() + '?mode=ro', uri=True, timeout=10)
        return con

    def put(self, value):
        if 'company' in value:
            validate(value)
            kind, company = 'Dataset', value['company']['id']
        elif value.get('record_type') in ('Report', 'Decision', 'Forecast', 'Outcome'):
            validate_record(value)
            kind, company = value['record_type'], value['company_id']
        else:
            raise ValueError('Store accepts validated datasets and generated records')
        digest = fingerprint(value)
        with closing(self._connect(write=True)) as con, con:
            con.execute('INSERT OR IGNORE INTO snapshots VALUES (?, ?, ?, ?, ?)',
                        (digest, kind, company, datetime.now(timezone.utc).isoformat(), json.dumps(value, sort_keys=True)))
        return digest

    def get(self, digest):
        with closing(self._connect()) as con:
            row = con.execute('SELECT body FROM snapshots WHERE digest = ?', (digest,)).fetchone()
        if row is None:
            raise ValueError('Snapshot not found')
        value = json.loads(row[0])
        if fingerprint(value) != digest:
            raise ValueError('Stored snapshot integrity check failed')
        return value

    def history(self, company_id=None):
        with closing(self._connect()) as con:
            query = 'SELECT digest, kind, company_id, created_at FROM snapshots'
            rows = con.execute(query + (' WHERE company_id = ?' if company_id else '') + ' ORDER BY created_at, digest',
                               (company_id,) if company_id else ()).fetchall()
        return [dict(zip(('digest','kind','company_id','created_at'), row)) for row in rows]
