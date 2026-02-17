#!/usr/bin/env python3
"""Print the current brick contract parsed from spec.md."""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
SPEC_PATH = ROOT / "spec.md"


def section_lines(name: str, text: str) -> list[str]:
    lines = text.splitlines()
    header = f"{name}:"
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i + 1
            break
    if start is None:
        return []

    out = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped in {"FILES:", "ACCEPTANCE CRITERIA:", "SCOPE:"}:
            break
        out.append(line)
    return out


def main() -> int:
    text = SPEC_PATH.read_text(encoding="utf-8")
    brick_name = ""
    for line in text.splitlines():
        if line.startswith("BRICK:"):
            brick_name = line.split(":", 1)[1].strip()
            break

    print("Brick Contract")
    print(f"brick: {brick_name}")

    files = [line[2:].strip() for line in section_lines("FILES", text) if line.strip().startswith("-")]
    print("allowed_files:")
    for path in files:
        print(f"- {path}")

    print("acceptance_criteria:")
    for line in section_lines("ACCEPTANCE CRITERIA", text):
        if line.strip():
            print(line)

    print("scope_rules:")
    for line in section_lines("SCOPE", text):
        if line.strip():
            print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
