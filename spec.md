BRICK: Brick T1 - Publishable workflow blueprint (no code examples)

FILES:
- spec.md
- README.md
- .gitignore
- manifest.md
- roadmap.md
- WORKFLOW.md
- BUILDER.md
- PROMPTS/BUILDER_PROMPT.md
- skeptic-gate.md
- state-schema.md
- src/
- tests/
- test-output.txt
- .pytest_cache/
- .workflow/
- skeptic_packet/README.md
- skeptic_packet/spec.md
- skeptic_packet/diff.patch
- skeptic_packet/diff.txt
- skeptic_packet/test_output.txt
- skeptic_packet/state_excerpt.json
- skeptic_verdict.md
- handover.md

ACCEPTANCE CRITERIA:
1) README plain-language clarity
- README explains every workflow term in plain language for non-technical users.

2) README onboarding completeness
- README tells a new non-technical user exactly:
  - where ideas go
  - which files to edit
  - how to create a brick spec
  - how brutal honesty is enforced
  - best-case and worst-case walkthrough

3) Generated artifacts ignored
- `.gitignore` blocks generated artifacts, including:
  - `handover` outputs
  - `skeptic_packet` outputs
  - `skeptic_verdict` outputs
  - snapshots
  - caches

4) Demo app code removed from template
- If src/ and tests/ exist and are demo-only, remove them.
- No application/demo code remains.

TEST REQUIREMENTS:
- N/A (this is documentation + repo hygiene only; no app behavior)

OUT OF SCOPE:
- Add example source code.
