# Roadmap (Planning Contract)

Use this file to plan work before execution. This is reusable across projects.

## Purpose

- Convert an idea into clear, scoped bricks.
- Keep `spec.md` deterministic and small.
- Define quality gates before implementation starts.

## Test Policy

- Feature bricks must include TEST REQUIREMENTS in spec.md (or N/A with reason).
- Skeptic should FAIL if required test categories are missing.

## Idea to Bricks

Planning pipeline:
- Idea -> PRD -> Brick Specs -> current `spec.md`

Rules:
- Keep one active brick in `spec.md` at a time.
- Every brick must include explicit file scope, acceptance criteria, and tests.
- Feature bricks must implement tests meeting the TEST REQUIREMENTS block; Skeptic should FAIL if missing.

## Co-Dev Roles

- Codex and Claude Code are both Builders.
- Both Builders follow `PROMPTS/BUILDER_PROMPT.md`.
- Skeptic can be ChatGPT, Gemini, or Claude Web.
- Skeptic must write repo-root `skeptic_verdict.md`.
- Approval requires the exact plain line: `Verdict: PASS`.

## Loop Stop Condition

- If `loop_count >= 3`, stop repeating the same brick.
- Rescope before any further implementation.

## PRD Template (max 1 page)

Copy/paste block:

```md
# PRD: <title>

## Problem
<what is broken or missing>

## Users
<who is affected>

## Success metrics
- <metric 1>
- <metric 2>

## Constraints
- <technical/business constraints>

## Non-goals
- <explicitly excluded work>

## Risks
- <top risk>
- <mitigation>
```

## Brick Spec Template (must be used to generate spec.md)

Copy/paste block:

```md
BRICK: <name>

FILES:
- <path 1>
- <path 2>

ACCEPTANCE CRITERIA:
- Given <initial state>
- When <action>
- Then <expected result>

TEST REQUIREMENTS:
- Happy path: <test case>
- Edge cases (>=2):
  - <edge 1>
  - <edge 2>
- Invalid input (>=1): <test case>
- Error handling (>=1): <test case>
- Side effects:
  - <side effect assertion>
# OR (only if truly applicable)
- N/A: <reason tests are not required for this brick>

OUT OF SCOPE:
- <excluded item>

ROLLBACK/UNDO plan:
- <undo step 1>
- <undo step 2>
- <undo step 3>
```

## Definition of Done

All must be true:
- Tests PASS.
- `verify_files_touched` PASS.
- `skeptic_packet` generated.
- `skeptic_verdict.md` contains exact line `Verdict: PASS`.
- `python3 tools/update_state.py --complete` succeeds.

## Context Rot Reset

Start a new chat when context degrades (long thread, conflicting instructions, repeated misunderstandings).

Paste this minimum reset packet:
- `manifest.md`
- current `spec.md`
- `state.json` excerpt (`current_brick`, `status`, `loop_count`, `last_gate_failed`, `last_test_run`)
