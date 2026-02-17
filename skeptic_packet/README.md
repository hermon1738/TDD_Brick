# Skeptic Packet

This folder provides deterministic inputs for Skeptic review.

Required files:
- `spec.md` (copy of repo-root `spec.md`)
- `diff.patch` or `diff.txt` (patch/diff of changes)
- `test_output.txt` (latest test output)
- `state_excerpt.json` (relevant excerpt from `state.json`)

Recommended diff command:
- `git diff > skeptic_packet/diff.patch`

The Skeptic verdict must be written to repo-root `skeptic_verdict.md`.
Approval is rejected unless `skeptic_verdict.md` contains `Verdict: PASS`.
