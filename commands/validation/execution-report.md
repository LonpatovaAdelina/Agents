---
description: Generate a report on what was built during the current execution session
argument-hint: [session-id or feature-name]
---

# Execution Report: What Was Built

## Overview

Produces a structured summary of everything created, modified, or deferred during an execution session. Used to hand off context between sessions, agents, or for user review.

Input: `$ARGUMENTS` — session identifier or feature name (optional, for labeling)

---

## Report Generation Steps

### Step 1 — Collect Session Artifacts
Scan for all changes made during this session:
- New files created
- Existing files modified
- Plans created or updated
- Documents updated (PRD, ARCHITECTURE, README)
- Issues resolved (from review or bug fix)

### Step 2 — Map to Requirements
For each artifact, link it to the originating requirement:
- Which FR (functional requirement) from PRD does it fulfill?
- Which user story does it close?
- Which plan subtask does it complete?

### Step 3 — Assess Completeness
For the session scope, evaluate:
- What was planned vs. what was delivered
- What was deferred and why
- What blockers were encountered

---

## Report Format

```
EXECUTION REPORT
================
Session: [label or timestamp]
Feature / Task: [name from $ARGUMENTS or inferred]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DELIVERED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files Created:
  + path/to/new-file.py         [FR-XX: description]
  + path/to/another-file.py     [FR-XX: description]

Files Modified:
  ~ path/to/existing-file.py    [what changed and why]

Requirements Closed:
  ✅ FR-01: [description]
  ✅ User Story: "As a [user]..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEFERRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 [item] — reason: [why deferred]
  📋 [item] — tracked in: plans/tech-debt.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOCKERS ENCOUNTERED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️  [blocker description] — resolved by: [action taken]
  🔴 [blocker description] — UNRESOLVED — needs: [what's required]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PIPELINE STATE AFTER SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Current stage: [e.g. "code generation — 60% complete"]
  Next recommended action: [specific command to run next]
  Pending validations: [list any validate.md runs needed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPEN ITEMS FOR USER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [ ] [decision or confirmation needed from user]
  [ ] [assumption that needs validation]
```

---

## Usage

Run at the end of every significant work session — especially before:
- Ending a session (context handoff)
- Switching agents or workstreams
- Requesting a human review
- Running `validate.md` on the full project
