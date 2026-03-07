---
description: High-level review of the entire system against PRD and architecture
argument-hint: [focus-area: all | requirements | design | integration]
---

# System Review: End-to-End Coherence Check

## Overview

A holistic review that goes beyond individual files — it checks whether the system as a whole delivers on its requirements, whether components fit together correctly, and whether the project is ready for delivery or the next phase.

Input: `$ARGUMENTS` — focus area (default: `all`)

---

## Review Dimensions

### 1. Requirements Coverage (`requirements`)
Verify that every PRD requirement is addressed somewhere in the codebase:

For each `✅ In Scope` item from PRD:
- [ ] It is implemented (not just stubbed)
- [ ] It maps to at least one file in `ARCHITECTURE.md`
- [ ] It has at least one user story with acceptance criteria
- [ ] It was included in an execution report

Flag any requirement with no clear implementation as `UNCOVERED`.

### 2. Design Integrity (`design`)
Verify that the implementation matches `ARCHITECTURE.md`:

- [ ] All planned modules exist
- [ ] No modules exist outside the architecture (shadow code)
- [ ] API contracts match between caller and callee
- [ ] Data models are consistent across modules
- [ ] No circular imports or dependency inversions
- [ ] Environment variables match the documented list

### 3. Integration Coherence (`integration`)
Verify that components work together:

- [ ] All inter-module interfaces are implemented on both sides
- [ ] External service integrations have error handling and fallbacks
- [ ] Auth flow works end-to-end (login → protected resource)
- [ ] Data flows correctly from entry point to persistence layer
- [ ] Background jobs / async processes are properly wired

### 4. Delivery Readiness (`all`)
Check whether the project is ready for handoff or deployment:

- [ ] `README.md` exists and is accurate
- [ ] All environment variables are documented
- [ ] No `[STUB]`, `[ASSUMED]`, or `# TODO:` items in critical paths
- [ ] `validate.md` has been run and passed
- [ ] Open Questions list is empty or all items are explicitly deferred
- [ ] `execution-report.md` is current

---

## Output Format

```
SYSTEM REVIEW
=============
Focus: [all | requirements | design | integration]
Run at: [timestamp]

REQUIREMENTS COVERAGE:
  ✅ Covered: XX / XX in-scope requirements
  ❌ Uncovered: [list with FR numbers]

DESIGN INTEGRITY:
  ✅ Matches architecture: X files
  ❌ Deviations found: [list with details]
  ⚠️  Warnings: [list]

INTEGRATION COHERENCE:
  ✅ Verified: [list of integration points checked]
  ❌ Broken: [list with description]

DELIVERY READINESS:
  ✅ Ready: [items that passed]
  ❌ Not Ready: [items that failed]
  ⚠️  Conditional: [items that are ok with caveats]

OVERALL VERDICT:
  🟢 READY FOR DELIVERY
  🟡 READY WITH CONDITIONS — [list conditions]
  🔴 NOT READY — [list blockers]

RECOMMENDED NEXT STEPS:
  1. [highest priority action]
  2. [second priority action]
```

---

## When to Run System Review

| Trigger | Expected Outcome |
|---------|-----------------|
| End of each implementation phase | Catch gaps before moving to next phase |
| Before user demo or stakeholder review | Ensure nothing is broken or missing |
| Before final delivery | Full green light check |
| After major architectural change | Verify nothing was broken by the change |
