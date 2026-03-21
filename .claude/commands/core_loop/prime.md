---
description: Prime the agent with full project context before starting work
argument-hint: [project-root-path]
---

# Prime: Load Project Context

## Overview

Run this command at the start of every new session or when switching between projects. It loads all relevant project documents and code context so the agent can work accurately without re-reading files mid-task.

Input: `$ARGUMENTS` — path to project root (default: current directory)

---

## What Priming Does

Priming is **not** code generation. It is a structured read phase that:
1. Builds a mental model of the project
2. Identifies the current state of the pipeline
3. Surfaces any blockers or inconsistencies before work begins
4. Prepares the agent to execute tasks without constant re-reads

---

## Priming Steps

### Step 1 — Read Core Documents (in order)
1. `AGENT.md` — agent roles and pipeline rules
2. `PRD.md` — product requirements (if exists)
3. `ARCHITECTURE.md` — technical design (if exists)
4. `README.md` — setup and context (if exists)

For each document, extract and hold in context:
- Current `status` field (if present)
- Open questions or `[ASSUMED]` items
- Key constraints that affect implementation

### Step 2 — Scan Project Structure
Walk the directory tree from `$ARGUMENTS`:
- Note which modules exist vs. which are planned but not yet created
- Identify files marked `[STUB]` or containing `# TODO:`
- Flag any files that exist but are not referenced in `ARCHITECTURE.md`

### Step 3 — Load Active Plans
Check `plans/` directory (if exists):
- List all plan files and their completion status
- Identify the next unstarted subtask across all plans
- Note any plans with unresolved blockers

### Step 4 — Assess Pipeline State
Determine where the project currently stands:

```
[ ] PRD created and confirmed
[ ] Architecture designed
[ ] Plans written for in-scope features
[ ] Core modules implemented
[ ] Review cycles completed
[ ] Documentation written
```

### Step 5 — Output Prime Report

```
PRIME REPORT
============
Project: [name from PRD or directory]
Primed at: [timestamp]

DOCUMENTS LOADED:
  ✅ PRD.md — [one-line summary of product]
  ✅ ARCHITECTURE.md — [one-line summary of stack]
  ⚠️  README.md — not found

PIPELINE STATE: [current stage]

NEXT RECOMMENDED ACTION:
  [specific next step, e.g. "Run plan-feature.md for FR-03: user authentication"]

OPEN ITEMS:
  - [ASSUMED] items needing user validation
  - Unresolved open questions from PRD
  - TODO items in code

BLOCKERS:
  - [list any blockers, or "none"]
```

---

## When to Re-Prime

Re-run `prime.md` when:
- Starting a new work session
- Switching to a different feature area
- After a `rollback` or major state change
- When the agent seems to be operating on stale context
