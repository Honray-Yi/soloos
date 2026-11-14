"""Build a self-contained, deterministic skill-only plugin and ZIP.

Source of truth: .agents/skills/soloos and packaging/plugin.json.
Never follows symlinks or replaces an existing output directory/archive.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(output, skill=None, archive=None):
    output = Path(output)
    skill = Path(skill) if skill else ROOT/'.agents/skills/soloos'
    if output.exists() or (archive and Path(archive).exists()):
        raise FileExistsError('Choose new plugin output and archive paths')
    manifest = json.loads((ROOT/'packaging/plugin.json').read_text(encoding='utf-8'))
    if manifest['name'] != skill.name or not (skill/'SKILL.md').is_file():
        raise ValueError('Invalid skill or manifest identity')
    entries = {'plugin.json': (json.dumps(manifest,indent=2)+'\n').encode('utf-8')}
    for file in sorted(skill.rglob('*')):
        if '__pycache__' in file.parts or file.suffix == '.pyc': continue
        if file.is_symlink(): raise ValueError('Plugin input must not contain symlinks')
        if file.is_file(): entries['skills/soloos/'+file.relative_to(skill).as_posix()] = file.read_bytes()
    entries['SHA256SUMS.json'] = (json.dumps({p: hashlib.sha256(b).hexdigest() for p,b in entries.items()},indent=2)+'\n').encode()
    output.mkdir(parents=True)
    for name, content in entries.items():
        path=output/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(content)
    if archive:
        archive=Path(archive); archive.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as bundle:
            for name,content in sorted(entries.items()):
                info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o644 << 16
                bundle.writestr(info,content)
    return output


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--skill',type=Path)
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    print(build(args.output,args.skill,args.archive))
