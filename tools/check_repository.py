"""Check publishable repository paths and local Markdown link targets.

Uses Git's ignore rules, so local environments and work artifacts are not scanned
or treated as distributable files. Does not claim to test prompt-model behavior.
"""
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]


def check():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0')
    names=sorted(set(filter(None,names)))
    problems=[]; checked_links=0
    for name in names:
        path=ROOT/name
        if path.is_symlink(): problems.append(name+': symlink is not a reviewed distribution file')
        if any(part in {'work','dist','.venv','__pycache__','.pytest_cache'} for part in Path(name).parts):
            problems.append(name+': local artifact would be uploaded')
        if not path.is_file():
            problems.append(name+': missing file'); continue
        if path.suffix.lower()!='.md': continue
        content=path.read_text(encoding='utf-8')
        for raw in re.findall(r'\]\(([^)]+)\)',content):
            target=raw.strip().strip('<>')
            if urlsplit(target).scheme or target.startswith('#'): continue
            relative=unquote(target.split('#',1)[0])
            if not relative: continue
            destination=(path.parent/relative).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                problems.append(f'{name}: broken/out-of-repo link {target}')
            checked_links += 1
    result={'publishable_files':len(names),'checked_local_links':checked_links,'problems':problems}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if problems else 0


if __name__=='__main__': raise SystemExit(check())
