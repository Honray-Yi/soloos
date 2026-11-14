import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest
from jsonschema import Draft202012Validator

from soloos.data import ROOT as SKILL

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_plugin',ROOT/'tools/build_plugin.py')
builder=importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)


def test_packaged_runtime_and_checksums(tmp_path):
    output=builder.build(tmp_path/'plugin',SKILL,tmp_path/'plugin.zip')
    hashes=json.loads((output/'SHA256SUMS.json').read_text())
    assert all(hashlib.sha256((output/path).read_bytes()).hexdigest()==digest for path,digest in hashes.items())
    with zipfile.ZipFile(tmp_path/'plugin.zip') as bundle:
        assert all('..' not in Path(name).parts for name in bundle.namelist())
        bundle.extractall(tmp_path/'unpacked')
    cli=tmp_path/'unpacked/skills/soloos/scripts/soloos_cli.py'
    run=subprocess.run([sys.executable,str(cli),'template','saas'],cwd=tmp_path,capture_output=True,text=True,timeout=30)
    assert run.returncode==0,run.stderr
    assert json.loads(run.stdout)['metrics'][0]['name']=='mrr_growth'
    with pytest.raises(FileExistsError): builder.build(output,SKILL)


def test_reproducible_archive_and_manifest(tmp_path):
    builder.build(tmp_path/'one',SKILL,tmp_path/'one.zip')
    builder.build(tmp_path/'two',SKILL,tmp_path/'two.zip')
    assert (tmp_path/'one.zip').read_bytes()==(tmp_path/'two.zip').read_bytes()
    manifest=json.loads((ROOT/'packaging/plugin.json').read_text())
    assert manifest['$schema']=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert manifest['name']=='soloos' and 'license' not in manifest
    assert not any(key in manifest for key in ['hooks','mcpServers'])
    schema=json.loads((ROOT/'packaging/agent-plugin.schema.json').read_text())
    Draft202012Validator(schema).validate(manifest)


def test_committed_distribution_matches_runtime():
    package=ROOT/'plugins/soloos'
    if not package.exists():
        pytest.skip('Generated distribution is not built in this development checkout')
    assert json.loads((package/'plugin.json').read_text()) == json.loads((ROOT/'packaging/plugin.json').read_text())
    runtime_files={p.relative_to(SKILL).as_posix():p.read_bytes() for p in SKILL.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    packaged=package/'skills/soloos'
    package_files={p.relative_to(packaged).as_posix():p.read_bytes() for p in packaged.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    assert runtime_files==package_files
    hashes=json.loads((package/'SHA256SUMS.json').read_text())
    assert all(hashlib.sha256((package/path).read_bytes()).hexdigest()==digest for path,digest in hashes.items())
