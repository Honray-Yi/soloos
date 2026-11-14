"""Copy a reviewed skill into a protected discovery directory without overwrites.

Run only when the destination write is authorized by the host. This is a local
development installation helper, not a plugin publisher or a permissions bypass.
"""

import argparse
from pathlib import Path
import shutil


def install(source, destination):
    source, destination = source.resolve(), destination.absolute()
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source is not a skill directory")
    paths = []
    for path in source.rglob("*"):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError("Symlinks are not accepted in the runtime source")
        if path.is_file():
            target = destination / path.relative_to(source)
            if any(parent.is_symlink() for parent in [target, *target.parents]):
                raise ValueError("Symlink destination is not accepted")
            if target.exists() and target.read_bytes() != path.read_bytes():
                raise FileExistsError(f"Refusing to overwrite different existing content: {target}")
            paths.append((path, target))
    copied = 0
    for path, target in paths:
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with path.open("rb") as reader, target.open("xb") as writer:
            shutil.copyfileobj(reader, writer)
        copied += 1
    print(f"Verified {len(paths)} runtime files; installed {copied} new files into {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    install(args.source, args.destination)
