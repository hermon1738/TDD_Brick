#!/usr/bin/env python3
"""Verify modified files stay within spec.md FILES scope.

Dual mode:
- Git mode: compare with `git diff HEAD --name-only`.
- Snapshot mode (no .git): compare current file hashes to
  `.workflow/snapshots/before.json`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
SPEC_PATH = ROOT / "spec.md"
SNAPSHOT_PATH = ROOT / ".workflow" / "snapshots" / "before.json"


def parse_allowed_files() -> set[str]:
    lines = SPEC_PATH.read_text(encoding="utf-8").splitlines()
    allowed = []
    in_files = False
    for line in lines:
        stripped = line.strip()
        if stripped == "FILES:":
            in_files = True
            continue
        if in_files and stripped.endswith(":") and not line.startswith(" "):
            break
        if in_files and stripped.startswith("-"):
            allowed.append(stripped[1:].strip())
    return set(allowed)


def has_git_repo() -> bool:
    if (ROOT / ".git").exists():
        return True
    if shutil.which("git") is None:
        return False

    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def modified_files_git() -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "HEAD", "--name-only"],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git diff failed")

    files = []
    for line in proc.stdout.splitlines():
        name = line.strip()
        if name:
            files.append(name)
    return files


def sha256_for(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def snapshot_target_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/"):
            continue
        if rel == ".workflow/snapshots/before.json":
            continue
        files.append(path)
    return files


def build_snapshot() -> dict[str, str]:
    data = {}
    for path in snapshot_target_files():
        rel = path.relative_to(ROOT).as_posix()
        data[rel] = sha256_for(path)
    return data


def write_snapshot() -> None:
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"files": build_snapshot()}
    SNAPSHOT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_snapshot() -> dict[str, str]:
    if not SNAPSHOT_PATH.exists():
        raise RuntimeError(
            "baseline missing: run `python3 tools/verify_files_touched.py --snapshot-init`"
        )
    payload = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    files = payload.get("files")
    if not isinstance(files, dict):
        raise RuntimeError(
            "invalid baseline format: run `python3 tools/verify_files_touched.py --snapshot-init`"
        )
    out = {}
    for key, value in files.items():
        if isinstance(key, str) and isinstance(value, str):
            out[key] = value
    return out


def modified_files_snapshot() -> list[str]:
    before = read_snapshot()
    now = build_snapshot()

    changed_or_added = []
    for path, digest in now.items():
        if path not in before or before[path] != digest:
            changed_or_added.append(path)
    return sorted(changed_or_added)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot-init",
        action="store_true",
        help="create baseline snapshot for non-git mode",
    )
    args = parser.parse_args()

    if args.snapshot_init:
        write_snapshot()
        print(f"SNAPSHOT_INIT_OK: {SNAPSHOT_PATH.relative_to(ROOT)}")
        return 0

    allowed = parse_allowed_files()
    try:
        if has_git_repo():
            changed = modified_files_git()
        else:
            changed = modified_files_snapshot()
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 2

    offenders = [path for path in changed if path not in allowed]

    if offenders:
        print("OUT OF SCOPE FILES DETECTED:")
        for path in offenders:
            print(f"- {path}")
        return 1

    print("OK: all touched files are in spec FILES list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
