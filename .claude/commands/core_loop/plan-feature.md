---
description: Break down a feature into an actionable implementation plan
argument-hint: [feature-name]
---

# Plan Feature: Create an Implementation Plan

## Overview

Takes a feature name or description and produces a detailed, step-by-step implementation plan that `execute.md` can act on directly.

Input: `$ARGUMENTS` — feature name or short description

---

## Planning Steps

### Step 1 — Locate in PRD
Find the feature in `PRD.md`:
- Identify the relevant user stories
- Extract functional requirements (FR-XX entries)
- Note any non-functional requirements that apply (performance, security)
- Check MVP scope — confirm this feature is ✅ In Scope

If the feature is not in the PRD — stop and ask the user whether to add it first.

### Step 2 — Map to Architecture
From `ARCHITECTURE.md`, identify:
- Which modules/components are involved
- What new files need to be created (with exact paths)
- What existing files need to be modified
- What interfaces or contracts are affected

### Step 3 — Define Subtasks
Break the feature into atomic subtasks. Each subtask must be:
- Completable in a single `execute` run
- Independently testable
- Clearly sequenced (note dependencies between subtasks)

Format:
```
SUBTASK-01: [name]
  Description: what exactly needs to be implemented
  Files: list of files to create or modify
  Inputs: what this subtask receives
  Outputs: what this subtask produces
  Depends on: SUBTASK-XX (or "none")
  Acceptance criteria:
    - criterion 1
    - criterion 2
```

### Step 4 — Identify Risks
For each subtask, note:
- Any unclear requirements that need resolution
- External dependencies (APIs, libraries) that may behave unexpectedly
- Performance or security considerations

### Step 5 — Output the Plan

Produce a plan file saved as `plans/[feature-name].md` with:
1. Feature summary (2–3 sentences)
2. Affected modules list
3. Ordered subtask list (from Step 3)
4. Risks and open questions
5. Estimated complexity: `low` | `medium` | `high`

---

## Plan Quality Checklist

- [ ] Every subtask maps to at least one FR from the PRD
- [ ] No subtask is larger than "one file or one function group"
- [ ] All file paths match `ARCHITECTURE.md`
- [ ] Dependencies between subtasks are explicit
- [ ] Open questions are listed, not silently assumed away
