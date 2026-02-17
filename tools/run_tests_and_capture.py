#!/usr/bin/env python3
"""Run project tests from context.txt, capture output, and update gate state."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CONTEXT_PATH = ROOT / "context.txt"
STATE_PATH = ROOT / "state.json"
HANDOVER_PATH = ROOT / "handover.md"
ARTIFACT_PATH = ROOT / "skeptic_packet" / "test_output.txt"


def load_state() -> dict:
    with STATE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict) -> None:
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def parse_test_command() -> str:
    for line in CONTEXT_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("TEST_COMMAND:"):
            cmd = line.split(":", 1)[1].strip()
            if cmd:
                return cmd
    raise ValueError("missing TEST_COMMAND in context.txt")


def extract_failed_nodeids(output: str) -> list[str]:
    nodeids = []
    patterns = [
        re.compile(r"^FAILED\s+([^\s]+)"),
        re.compile(r"^ERROR\s+at setup of\s+([^\s]+)"),
        re.compile(r"^ERROR\s+([^\s]+)"),
    ]

    for line in output.splitlines():
        text = line.strip()
        for pattern in patterns:
            match = pattern.match(text)
            if match:
                nodeid = match.group(1).strip()
                if "::" in nodeid or nodeid.endswith(".py"):
                    nodeids.append(nodeid)
                break

    unique = []
    for item in nodeids:
        if item not in unique:
            unique.append(item)
    return unique


def run_command(command: str) -> tuple[int, str, str | None]:
    argv = shlex.split(command)
    if not argv:
        return 2, "", "empty TEST_COMMAND"

    try:
        proc = subprocess.run(
            argv,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout, None
    except FileNotFoundError as exc:
        missing = exc.filename or argv[0]
        return 127, f"tool not found: {missing}\n", missing


def detect_missing_tool_from_output(output: str) -> str | None:
    for line in output.splitlines():
        text = line.strip()
        if "No module named " in text:
            return text.split("No module named ", 1)[1].strip("'\"")
        if "command not found" in text and ":" in text:
            return text.rsplit(":", 1)[-1].replace("command not found", "").strip()
    return None


def short_reason(exit_code: int, failed_nodeids: list[str], missing_tool: str | None) -> str:
    if missing_tool:
        return f"missing tool {missing_tool}"
    if failed_nodeids:
        return f"failing nodeid {failed_nodeids[0]}"
    return f"missing tool unknown (exit {exit_code})"


def append_handover(command: str, status: str, exit_code: int, reason: str | None) -> None:
    lines = [
        "",
        "## TEST GATE",
        f"- command: `{command}`",
        f"- status: {status}",
        f"- exit_code: {exit_code}",
    ]
    if reason:
        lines.append(f"- reason: {reason}")
    lines.append(f"- artifact: `{ARTIFACT_PATH.relative_to(ROOT)}`")
    with HANDOVER_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> int:
    state = load_state()

    try:
        command = parse_test_command()
    except ValueError as exc:
        ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT_PATH.write_text(str(exc) + "\n", encoding="utf-8")

        state["last_test_run"] = {
            "command": "",
            "status": "FAIL",
            "exit_code": 2,
            "artifact": str(ARTIFACT_PATH.relative_to(ROOT)),
            "failed_nodeids": [],
        }
        state["last_gate_failed"] = "TEST: missing tool TEST_COMMAND"
        state["loop_count"] = int(state.get("loop_count", 0)) + 1
        save_state(state)

        append_handover("", "FAIL", 2, "missing TEST_COMMAND in context.txt")
        print("FAIL: missing TEST_COMMAND in context.txt")
        return 2

    exit_code, output, missing_tool = run_command(command)
    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_PATH.write_text(output, encoding="utf-8")

    failed_nodeids = extract_failed_nodeids(output)
    if missing_tool is None:
        missing_tool = detect_missing_tool_from_output(output)
    status = "PASS" if exit_code == 0 else "FAIL"

    state["last_test_run"] = {
        "command": command,
        "status": status,
        "exit_code": exit_code,
        "artifact": str(ARTIFACT_PATH.relative_to(ROOT)),
        "failed_nodeids": failed_nodeids,
    }

    reason = None
    if status == "PASS":
        state["last_gate_failed"] = None
    else:
        reason = short_reason(exit_code, failed_nodeids, missing_tool)
        state["last_gate_failed"] = f"TEST: {reason}"
        state["loop_count"] = int(state.get("loop_count", 0)) + 1

    save_state(state)
    append_handover(command, status, exit_code, reason)

    print(status)
    print(f"command: {command}")
    print(f"artifact: {ARTIFACT_PATH.relative_to(ROOT)}")
    return 0 if status == "PASS" else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
