# SKEPTIC GATE (MANDATORY)

Use this gate before approving any Architect output. Do not skip.

## Required Inputs

- `skeptic_packet/spec.md` (copy of repo-root `spec.md`)
- `skeptic_packet/diff.patch` or `skeptic_packet/diff.txt` (patch/diff; prefer `git diff > skeptic_packet/diff.patch`)
- `skeptic_packet/test_output.txt` (latest test output file)
- `skeptic_packet/state_excerpt.json` (relevant `state.json` excerpt)

If any required input is missing, return:
- `Verdict: FAIL`
- `Could fail because: missing required skeptic inputs`

## Verdict Output Location

- Write the final verdict to repo-root `skeptic_verdict.md`.
- The verdict file must include `Verdict: PASS` or `Verdict: FAIL`.
- In `skeptic_verdict.md`, the verdict line must be written as a plain line (no bullets), exactly as `Verdict: PASS` or `Verdict: FAIL`.
- Approval flows only accept `Verdict: PASS` in `skeptic_verdict.md`.

## Decision

- PASS: only if every section below is addressed with concrete evidence.
- FAIL: if any section is weak, missing, or unclear.

## 1) Flaw Hunt

- What is incorrect, inefficient, or over-engineered?
- What breaks first under normal usage?
- What hidden assumptions is Architect making?

Required output:
- `Critical flaws:` ...
- `Non-critical flaws:` ...

## 2) Blind Spot Hunt

- What scenarios are missing from tests?
- What edge cases are not covered?
- What operational concerns are ignored (observability, rollback, migration)?

Required output:
- `Blind spots:` ...

## 3) Long-Term Scaling Check

Run this section only if one or more conditions are true:
- a new module is introduced
- data model or persistence behavior changes
- an external dependency is added
- API contract or architecture boundary changes

If none are true, output:
- `Scaling risks: N/A (not applicable for this brick)`

- What fails at 10x load, data size, or team size?
- Which design choices create future lock-in?
- Where will maintenance cost grow fastest?

Required output:
- `Scaling risks:` ...

## 4) Failure-First Challenge

Before any agreement, provide one reason the approach could fail.

Required output:
- `Could fail because:` ...

## 5) Honesty Constraint

- No motivational fluff.
- No filler phrases.
- If uncertain, write exactly: `UNCERTAIN`.

## Final Gate Output Template

- `Verdict: PASS|FAIL`
- `Could fail because: ...`
- `Critical flaws: ...`
- `Blind spots: ...`
- `Scaling risks: ...`
- `Required fixes before PASS: ...`
