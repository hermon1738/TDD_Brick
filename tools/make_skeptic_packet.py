#!/usr/bin/env python3
"""Generate skeptic packet artifacts deterministically from repo root."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
PACKET_DIR = ROOT / "skeptic_packet"
SPEC_SRC = ROOT / "spec.md"
STATE_SRC = ROOT / "state.json"

TEST_CMD = ["python3", "-m", "pytest", "-q"]
STATE_KEYS = [
    "current_brick",
    "status",
    "loop_count",
    "last_gate_failed",
    "last_test_run",
]


def write_spec_copy() -> Path:
    dst = PACKET_DIR / "spec.md"
    shutil.copyfile(SPEC_SRC, dst)
    return dst


def write_state_excerpt() -> Path:
    dst = PACKET_DIR / "state_excerpt.json"
    with STATE_SRC.open("r", encoding="utf-8") as f:
        state = json.load(f)

    excerpt = {k: state.get(k) for k in STATE_KEYS if k in state}
    with dst.open("w", encoding="utf-8") as f:
        json.dump(excerpt, f, indent=2)
        f.write("\n")
    return dst


def write_test_output() -> tuple[Path, int]:
    dst = PACKET_DIR / "test_output.txt"
    proc = subprocess.run(
        TEST_CMD,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    with dst.open("w", encoding="utf-8") as f:
        f.write(proc.stdout)
    return dst, proc.returncode


def is_git_repo() -> bool:
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


def write_diff_artifact() -> Path:
    patch_path = PACKET_DIR / "diff.patch"
    text_path = PACKET_DIR / "diff.txt"

    if is_git_repo():
        proc = subprocess.run(
            ["git", "diff"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        with patch_path.open("w", encoding="utf-8") as f:
            f.write(proc.stdout)
        if text_path.exists():
            text_path.unlink()
        return patch_path

    message = (
        "git diff unavailable: 'git' is not installed or current directory "
        "is not a git repository.\n"
    )
    with text_path.open("w", encoding="utf-8") as f:
        f.write(message)
    if patch_path.exists():
        patch_path.unlink()
    return text_path


def main() -> int:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)

    written_spec = write_spec_copy()
    written_state = write_state_excerpt()
    written_test, test_exit = write_test_output()
    written_diff = write_diff_artifact()

    print("Skeptic packet updated:")
    print(f"- {written_spec.relative_to(ROOT)}")
    print(f"- {written_state.relative_to(ROOT)}")
    print(f"- {written_test.relative_to(ROOT)} (test exit {test_exit})")
    print(f"- {written_diff.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
