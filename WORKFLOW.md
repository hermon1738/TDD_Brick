# Workflow SOP (Execution)

This file is the execution procedure. Use it after planning is done in `roadmap.md`.

## Preconditions

- Run from repo root.
- `spec.md` exists and defines current brick scope.
- `spec.md` must include `TEST REQUIREMENTS` unless explicitly `N/A` with a reason.
- Builder follows `PROMPTS/BUILDER_PROMPT.md`.

## Exact Command Sequence (per brick)

1. `python3 tools/print_brick_contract.py`
2. If `.git` is missing in repo root, run once before edits:
   `python3 tools/verify_files_touched.py --snapshot-init`
3. Implement brick changes (only files in `spec.md`).
4. `python3 tools/verify_files_touched.py`
5. `python3 tools/run_tests_and_capture.py`
6. `python3 tools/make_skeptic_packet.py`
7. Skeptic writes repo-root `skeptic_verdict.md`.
8. `python3 tools/update_state.py --complete`

## Test Gate Standard

- Feature bricks: require happy path + >=2 edge + >=1 invalid input + >=1 error handling + side effects (or N/A with reason)
- Bugfix bricks: require regression test first + coverage for the fix + side effects if any
- Tooling bricks: minimal tests only with explicit N/A justification in spec
- Side effects include filesystem/network/DB writes, global state mutations, or observable outputs beyond return values.

## Worked Example: Perfect Cycle

Commands:
- `python3 tools/print_brick_contract.py`
- `python3 tools/verify_files_touched.py`
- `python3 tools/run_tests_and_capture.py`
- `python3 tools/make_skeptic_packet.py`
- Skeptic writes `skeptic_verdict.md` with exact `Verdict: PASS`
- `python3 tools/update_state.py --complete`

Files created/updated:
- `skeptic_packet/spec.md` updated
- `skeptic_packet/test_output.txt` updated
- `skeptic_packet/state_excerpt.json` updated
- `skeptic_packet/diff.patch` or `skeptic_packet/diff.txt` updated
- `skeptic_verdict.md` created/updated with PASS line
- `state.json` updated to completed state:
  - `status: COMPLETED`
  - `last_gate_failed: null`
  - `loop_count: 0`

Next action:
- Select and prepare next brick.

## Worked Example: Failure Cycle

Failure path A (tests fail):
- Run `python3 tools/run_tests_and_capture.py`
- `skeptic_packet/test_output.txt` shows failure output
- `state.json` updated with:
  - `last_gate_failed: TESTS`
  - `last_test_run.status: FAIL`
  - `last_test_run.exit_code: <non-zero>`
  - `last_test_run.failed_nodeids: <if available>`
  - `last_test_run.summary: <short failure summary>`
  - `loop_count` incremented
- Run `python3 tools/make_skeptic_packet.py`
- Fix implementation, re-run sequence from verify step.

Failure path B (skeptic FAIL):
- Skeptic writes `skeptic_verdict.md` with `Verdict: FAIL`
- Run `python3 tools/update_state.py --complete`
- Completion is rejected; `state.json` remains in progress and `loop_count` increments.
- Address skeptic findings, regenerate packet, request another skeptic pass.

## Rescope Protocol (`loop_count >= 3`)

When `loop_count >= 3`, stop implementation and rewrite `spec.md` before continuing.

Rewrite rules:
- Split the brick into smaller scope.
- Add explicit Non-goals.
- Tighten acceptance criteria (Given/When/Then).
- Add missing test requirements.

Must append this block to `handover.md`:

```md
## RESCOPE NOTE
- reason: loop_count reached 3 or more
- previous_brick: <name>
- rescope_action: split/tighten spec
- new_constraints: <non-goals, acceptance updates>
- next_action: prepare revised spec.md
```

## Context Rot SOP

Start a new chat if execution context is stale or contradictory.

Paste at minimum:
- `manifest.md`
- current `spec.md`
- `state.json` excerpt (`current_brick`, `status`, `loop_count`, `last_gate_failed`, `last_test_run`)
