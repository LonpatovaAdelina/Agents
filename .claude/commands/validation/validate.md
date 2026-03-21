---
description: Run full validation of the current project state
argument-hint: [scope: all | prd | architecture | code]
---

# Validate: Full Project Validation

## Overview

Runs a structured validation sweep across the specified scope. Produces a validation report with pass/fail status and a prioritized list of issues.

Input: `$ARGUMENTS` — scope to validate (default: `all`)

---

## Validation Scopes

### `prd` — Requirements Validation
Check that `PRD.md` is complete and internally consistent:

- [ ] All required sections are present (Executive Summary through Appendix)
- [ ] Every user story has acceptance criteria
- [ ] All `[ASSUMED]` items are flagged for user confirmation
- [ ] No contradictions between Goals and MVP Scope
- [ ] Non-functional requirements have measurable targets (not "should be fast")
- [ ] Open Questions section is current (resolved items removed)
- [ ] Success criteria are testable

### `architecture` — Design Validation
Check that `ARCHITECTURE.md` is coherent and implementable:

- [ ] Every component in the diagram has a corresponding module definition
- [ ] All file paths follow a consistent naming convention
- [ ] API contracts (request/response shapes) are fully defined
- [ ] No circular dependencies in the module graph
- [ ] Tech stack choices are justified and compatible
- [ ] Environment variables are listed completely
- [ ] Architecture covers all `✅ In Scope` items from PRD

### `code` — Implementation Validation
Check that generated code matches the plan:

- [ ] All files listed in `ARCHITECTURE.md` exist
- [ ] No files exist that are not listed in `ARCHITECTURE.md`
- [ ] No `[STUB]` markers remain in files (unless intentional and documented)
- [ ] All `# TODO:` items are tracked in Open Questions or plans
- [ ] No hardcoded secrets, API keys, or environment-specific URLs
- [ ] Error handling present for all external calls (API, DB, file I/O)
- [ ] All public functions/methods have docstrings or type hints
- [ ] No unused imports or dead code blocks

### `all` — Full Sweep
Runs `prd` → `architecture` → `code` in sequence.

---

## Output Format

```
VALIDATION REPORT
=================
Scope: [prd | architecture | code | all]
Run at: [timestamp]

SUMMARY:
  ✅ Passed: XX checks
  ❌ Failed: XX checks
  ⚠️  Warnings: XX items

FAILURES (must fix before proceeding):
  [SECTION] Check description
  → Issue: what exactly is wrong
  → Fix: what needs to be done

WARNINGS (should fix, not blocking):
  [SECTION] Check description
  → Issue: what's suboptimal
  → Recommendation: suggested improvement

ASSUMED ITEMS PENDING CONFIRMATION:
  - [list of [ASSUMED] tags found in PRD or architecture]

OVERALL STATUS: PASS | FAIL | PASS WITH WARNINGS
```

---

## When to Run Validate

| Trigger | Recommended Scope |
|---------|------------------|
| Before starting `execute.md` | `prd` + `architecture` |
| After completing a feature | `code` |
| After `implement-fix.md` | `code` |
| Before final delivery | `all` |
| After PRD is updated | `prd` |
