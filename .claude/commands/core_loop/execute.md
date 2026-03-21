---
description: Execute a planned feature or task end-to-end
argument-hint: [feature-name or task-id]
---

# Execute: Run a Planned Task to Completion

## Overview

Takes a planned task (from `plan-feature.md` output or a direct description) and executes it fully — generating all required code, wiring it into the project, and confirming completion.

Input: `$ARGUMENTS` — feature name, task ID, or path to plan file

---

## Pre-Execution Checklist

Before writing any code, verify:
- [ ] `PRD.md` exists and is confirmed by user
- [ ] `ARCHITECTURE.md` exists and defines the target module
- [ ] No conflicting work is in progress (check `status` in pipeline state)
- [ ] Dependencies for this task are already implemented or mocked

If any check fails — stop and report which condition is not met.

---

## Execution Steps

### Step 1 — Load Context
Read and internalize:
1. The task description or plan file (`$ARGUMENTS`)
2. Relevant sections of `PRD.md` (functional requirements, user stories)
3. Target module definition from `ARCHITECTURE.md`
4. Existing code in the affected directory (if any)

### Step 2 — Clarify Ambiguities
If the task description is ambiguous on any of these points, ask before proceeding:
- What is the exact input/output contract for this module?
- Are there edge cases explicitly called out in the PRD?
- Does this touch any shared utilities or interfaces?

Ask max **3 questions**. If everything is clear — proceed without asking.

### Step 3 — Implement
- Generate code file by file, following paths from `ARCHITECTURE.md`
- Each file must be complete and runnable — no placeholder bodies
- Use `# TODO:` only for items explicitly deferred by design
- Do not introduce new dependencies without flagging them

### Step 4 — Self-Review
Before handing off to `reviewer`, check:
- [ ] All acceptance criteria from the plan are addressed
- [ ] No hardcoded secrets or environment-specific values
- [ ] Error handling is present for all external calls
- [ ] Code matches the style of existing files in the project

### Step 5 — Report Completion
Output a structured summary:

```
TASK: [task name]
STATUS: complete | partial | blocked
FILES CREATED:
  - path/to/file.py
  - path/to/file.py
FILES MODIFIED:
  - path/to/file.py
DEFERRED (TODO items):
  - description of what was deferred and why
NOTES:
  - anything the reviewer or next agent should know
```

---

## Failure Modes

| Situation | Action |
|-----------|--------|
| Requirement is contradictory | Stop, flag contradiction, ask user to resolve |
| Needed module doesn't exist yet | Implement stub, mark as `[STUB]`, continue |
| Task scope expands mid-execution | Stop, update plan, get confirmation before continuing |
| Cannot implement without new dependency | Flag it, propose the dependency, wait for approval |
