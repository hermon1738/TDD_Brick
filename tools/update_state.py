#!/usr/bin/env python3
"""Update brick state, including skeptic completion gate enforcement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path.cwd()
STATE_PATH = ROOT / "state.json"
VERDICT_PATH = ROOT / "skeptic_verdict.md"
HANDOVER_PATH = ROOT / "handover.md"


def load_state() -> dict:
    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def has_pass_verdict() -> bool:
    if not VERDICT_PATH.exists():
        return False
    lines = VERDICT_PATH.read_text(encoding="utf-8").splitlines()
    return any(line.strip() == "Verdict: PASS" for line in lines)


def append_handover(lines: list[str]) -> None:
    with HANDOVER_PATH.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")


def reject_completion(state: dict) -> int:
    state["status"] = "IN_PROGRESS"
    state["last_gate_failed"] = "SKEPTIC: verdict missing PASS"
    state["loop_count"] = int(state.get("loop_count", 0)) + 1
    save_state(state)

    append_handover(
        [
            "## COMPLETION GATE",
            "- result: REJECTED",
            "- reason: SKEPTIC: verdict missing PASS",
            f"- brick: {state.get('current_brick', '')}",
            f"- status: {state.get('status', '')}",
            f"- loop_count: {state.get('loop_count', 0)}",
        ]
    )
    print("REJECTED: SKEPTIC: verdict missing PASS")
    return 1


def complete_brick(state: dict) -> int:
    state["status"] = "COMPLETED"
    state["last_gate_failed"] = None
    state["loop_count"] = 0

    current = state.get("current_brick", "")
    completed = state.get("completed_bricks")
    if not isinstance(completed, list):
        completed = []
    if current and current not in completed:
        completed.append(current)
    state["completed_bricks"] = completed

    state["next_action"] = "Select and prepare next brick"
    save_state(state)

    append_handover(
        [
            "## COMPLETION GATE",
            "- result: COMPLETED",
            f"- brick: {current}",
            "- status: COMPLETED",
            "- last_gate_failed: null",
            "- loop_count: 0",
            "- next_action: Select and prepare next brick",
        ]
    )
    print("COMPLETED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete", action="store_true", help="run completion gate")
    args = parser.parse_args()

    if not args.complete:
        parser.error("only --complete is supported")

    state = load_state()
    if not has_pass_verdict():
        return reject_completion(state)
    return complete_brick(state)


if __name__ == "__main__":
    raise SystemExit(main())
