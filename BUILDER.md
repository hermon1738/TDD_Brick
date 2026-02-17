# Builder Rules

## Hard Rules
- Operate only from the repository root.
- Canonical prompt file path is `PROMPTS/BUILDER_PROMPT.md` (do not use a repo-root `BUILDER_PROMPT.md`).
- If spec.md is not present in the current working directory: output exactly `UNCERTAIN: not in repo root` and stop.
- Read `BUILDER.md`, `spec.md`, `state.json`, and `context.txt` before editing.
- Do not assume roadmap.md exists; only read it if present.
- Implement only the current brick requirements in `spec.md`.
- Do not modify files outside the `FILES` list in `spec.md`.
- Do not change application code for workflow/tooling bricks.
- Do not weaken skeptic gates.
- If any instruction is ambiguous, stop and output exactly `UNCERTAIN`.

## Required Command Sequence
Run these commands in order:
1. `python3 tools/print_brick_contract.py`
2. If no `.git` in repo root, run once before edits: `python3 tools/verify_files_touched.py --snapshot-init`
3. Implement the brick changes
4. `python3 tools/verify_files_touched.py`
5. `python3 tools/run_tests_and_capture.py`
6. `python3 tools/make_skeptic_packet.py`

## Completion Notes
- A passing test gate does not by itself complete a brick.
- Completion is controlled by `python3 tools/update_state.py --complete`.
