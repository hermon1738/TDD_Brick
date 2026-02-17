
# Publishable Workflow Blueprint (No App Code)

This repository is a reusable workflow template for planning, implementing, reviewing, and approving work in small pieces called **bricks**.

It works with:
- Codex
- Claude Code
- ChatGPT
- Or manually

The rules stay the same regardless of tool.

---

# START HERE (First Time Setup)

## Step 1 — Go to Repository Root

The **repository root** is the folder that contains:

- `spec.md`
- `manifest.md`
- `roadmap.md`
- `WORKFLOW.md`

Check you are in the correct folder:

```bash
python3 -c "from pathlib import Path; print('OK' if Path('spec.md').exists() else 'NOT ROOT')"
````

If it prints `OK`, you are in the right place.

---

## Step 2 — Initialize Scope Tracking (If No Git)

If your project does NOT have a `.git` folder:

```bash
python3 tools/verify_files_touched.py --snapshot-init
```

This creates a baseline snapshot so the workflow can detect out-of-scope edits.

You only run this once.

---

# What This Repository Is

This repository does NOT contain an application.

It is a **workflow system**.

It forces you to:

1. Plan before building
2. Work in small pieces
3. Produce evidence
4. Get independent review
5. Complete safely

---

# Plain Language Definitions

**Idea**
Something you want to build or improve.

**PRD (Product Requirement Document)**
A short explanation of:

* What problem exists
* Who it affects
* What success looks like
* What is NOT included

**Roadmap (`roadmap.md`)**
Where ideas are structured into plans.

**Brick**
One small, clearly defined unit of work.

**Spec (`spec.md`)**
The active brick contract.

**FILES section**
The only files allowed to change for that brick.

**Acceptance Criteria**
Clear statements of what must be true when done.

**Test Requirements**
Required test categories (or explicit N/A with reason).

**Out of Scope**
What is explicitly forbidden for this brick.

**Builder**
The implementer (you or an AI).

**Skeptic**
Independent reviewer that challenges the work.

**Skeptic Packet (`skeptic_packet/`)**
Evidence bundle created before review.

**Verdict (`skeptic_verdict.md`)**
Skeptic decision file.
Must contain EXACT line:

```
Verdict: PASS
```

**State (`state.json`)**
Tracks:

* current brick
* failures
* loop_count
* test results

**loop_count**
If it reaches 3 → you must rescope the brick.

**Handover (`handover.md`)**
Local run log.
Not committed.
May not exist in fresh clone.

---

# Where Ideas Go

All new ideas start in:

```
roadmap.md
```

Never start in `spec.md`.

---

# How To Turn an Idea Into a Brick

1. Open `roadmap.md`
2. Write a short PRD
3. Define a small brick from it
4. Copy brick into `spec.md`
5. Only one active brick at a time

---

# What Files Do I Send to AI?

When starting a new chat with Codex or Claude Code, paste:

* `manifest.md`
* current `spec.md`
* short excerpt from `state.json`:

  * current_brick
  * status
  * loop_count
  * last_gate_failed
  * last_test_run

Optional but helpful:

* `roadmap.md`
* `WORKFLOW.md`

This prevents context rot and gives the AI full execution rules.

---

# Example Scenario (Non-Technical Walkthrough)

Imagine you want to build something simple:

> "I want a small script that counts words in a text file."

You have no code yet.

---

## Step 1 — Write PRD in roadmap.md

You write:

```
Problem:
No simple way to count words in a text file.

Users:
Anyone needing quick word counts.

Success:
Script prints word count for provided file.

Constraints:
Must be CLI-based.

Non-goals:
No GUI.
```

---

## Step 2 — Create First Brick in spec.md

Example brick:

```
BRICK: Word Counter CLI

FILES:
- src/word_counter.py
- tests/test_word_counter.py

ACCEPTANCE CRITERIA:
- Given a valid text file
- When running script
- Then prints correct word count

TEST REQUIREMENTS:
- Happy path
- >=2 edge cases
- >=1 invalid input
- >=1 error handling
- Side effects (CLI output)

OUT OF SCOPE:
- GUI
```

---

## Step 3 — Use Builder (Codex or Claude Code)

Paste `PROMPTS/BUILDER_PROMPT.md` into the tool.

The tool must:

* Follow sequence exactly
* Touch only files listed
* Generate skeptic packet

---

## Step 4 — Run Commands

```bash
python3 tools/print_brick_contract.py
python3 tools/verify_files_touched.py
python3 tools/run_tests_and_capture.py
python3 tools/make_skeptic_packet.py
```

You now have:

```
skeptic_packet/
```

---

## Step 5 — Skeptic Review

Send Skeptic:

* `skeptic_packet/spec.md`
* `skeptic_packet/test_output.txt`
* `skeptic_packet/state_excerpt.json`
* `skeptic_packet/diff.txt`
* `skeptic-gate.md`

Skeptic writes:

```
skeptic_verdict.md
```

If approved, it must contain:

```
Verdict: PASS
```

---

## Step 6 — Complete

```bash
python3 tools/update_state.py --complete
```

If valid, `state.json` shows:

* status: COMPLETED
* loop_count: 0

You move to next brick.

---

# Best-Case Scenario

* Verify passes
* Tests pass
* Skeptic writes PASS
* State completes
* Next brick begins

---

# Worst-Case Scenario

### Tests Fail

* Tests fail
* loop_count increases
* You fix implementation
* Repeat

### Skeptic Fails

* Skeptic writes FAIL
* Completion rejected
* loop_count increases
* Fix scope or logic
* Regenerate packet
* Retry review

### loop_count == 3

Stop.
Rewrite spec.
Reduce scope.
Try again.

---

# What Happens If I Switch From Codex to Claude?

Nothing changes.

Both must:

* Follow `PROMPTS/BUILDER_PROMPT.md`
* Run the same commands
* Generate the same skeptic packet
* Pass the same gates

Workflow is tool-independent.

---

# What This Template Does NOT Include

* No demo application code
* No example source files
* No compiled artifacts
* No built outputs

It is purely the workflow system.

You bring your own project.

---

# Final Rule

Small bricks pass.
Large bricks fail.

When in doubt, reduce scope.


***I built this shit. Me. Brick by brick. And I'll be damned if I let you tear it down just because you don't like the way another [N!\*\*@] talks!!!***

