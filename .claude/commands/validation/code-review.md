---
description: Perform a structured code review on generated or modified files
argument-hint: [file-path or directory]
---

# Code Review: Structured Review Pass

## Overview

Reviews code for correctness, security, consistency, and alignment with PRD and architecture. Produces structured feedback that `code-review-fix.md` can act on directly.

Input: `$ARGUMENTS` — file path, directory, or "all" for full project review

---

## Review Dimensions

### 1. Correctness
- Does the code implement what the PRD and architecture describe?
- Are edge cases handled (empty input, null values, max limits)?
- Is error handling present and meaningful (not bare `except: pass`)?
- Are all acceptance criteria from the relevant user story met?

### 2. Security
- No hardcoded secrets, tokens, or passwords
- No SQL/command injection vectors
- Input validation present on all external inputs
- Auth checks in place on all protected endpoints
- Sensitive data not logged

### 3. Consistency
- Naming follows project conventions (check existing files as reference)
- File structure matches `ARCHITECTURE.md`
- Import style consistent with rest of codebase
- Error response format consistent with other endpoints/modules

### 4. Maintainability
- Functions are single-purpose and reasonably sized (<50 lines as guideline)
- Complex logic has a brief comment explaining intent (not mechanics)
- No copy-paste duplication — shared logic is extracted
- No magic numbers or strings without named constants

### 5. Performance (flag only, don't optimize prematurely)
- N+1 query patterns in loops
- Unbounded operations on large collections
- Missing pagination on list endpoints
- Synchronous calls where async would be required at scale

---

## Review Output Format

For each issue found:

```
REVIEW ITEM
===========
FILE: path/to/file.py
LINE: XX (or range XX–YY)
DIMENSION: correctness | security | consistency | maintainability | performance
SEVERITY: critical | major | minor
ISSUE:
  [Clear description of what's wrong]
SUGGESTION:
  [Concrete recommendation — ideally with a code example]
```

### Severity Definitions
- **critical** — blocks sign-off; must be fixed before the code ships
- **major** — should be fixed in this iteration; not a blocker but important
- **minor** — noted for awareness; can be deferred to a cleanup task

---

## Summary Section

After all items, output:

```
REVIEW SUMMARY
==============
Files reviewed: X
Total issues: X (critical: X, major: X, minor: X)

SIGN-OFF STATUS: ✅ Approved | ❌ Changes Required

NEXT STEP:
  → Run code-review-fix.md to address critical and major items
  [or]
  → No action required — proceed to documenter
```

---

## Review Principles

- Review what the code **does**, not how you would have written it differently
- Do not request style changes that aren't part of project conventions
- Do not suggest refactors unless they fix a concrete problem
- Be specific — "this is unclear" is not actionable; explain why and what to do
