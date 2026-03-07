---
description: Apply fixes from a code review report
argument-hint: [review-report-path]
---

# Code Review Fix: Apply Review Feedback

## Overview

Takes the output of `code-review.md` and systematically applies all `critical` and `major` fixes. Minor items are logged but not acted on unless explicitly requested.

Input: `$ARGUMENTS` — path to review report (default: most recent review output)

---

## Pre-Fix Checklist

- [ ] Review report exists and is complete
- [ ] All `critical` issues are understood (not just copied)
- [ ] No open questions about what a fix should do

If a review item is unclear — ask one targeted question before fixing, not after.

---

## Fix Process

### Step 1 — Triage the Report
Group issues by file and severity:

```
critical fixes needed:  X items across Y files
major fixes needed:     X items across Y files
minor (deferred):       X items — logged, not actioned
```

### Step 2 — Fix Critical Items First
For each critical item:
1. Re-read the original code and the review suggestion
2. Understand *why* it's critical, not just what to change
3. Apply the minimal fix that resolves the issue
4. Mark it resolved in the tracking list

### Step 3 — Fix Major Items
For each major item:
1. Apply fix following the same approach
2. If fixing a major item would require touching >3 files, flag it before proceeding

### Step 4 — Log Minor Items
For each minor item, add to `plans/tech-debt.md` (create if doesn't exist):
```
DEFERRED ITEM
File: path/to/file.py
Issue: [description]
Severity: minor
Source: code-review [timestamp]
```

### Step 5 — Re-Review Changed Files
After applying all fixes, do a quick self-check on every modified file:
- Did the fix introduce any new issues?
- Is the fix consistent with other parts of the file?
- Does it align with the architecture?

### Step 6 — Output Fix Summary

```
CODE REVIEW FIX SUMMARY
========================
Review report: [path]

FIXES APPLIED:
  ✅ [FILE:LINE] — [one-line description of fix]
  ✅ [FILE:LINE] — [one-line description of fix]

DEFERRED TO TECH DEBT:
  📋 X minor items added to plans/tech-debt.md

ITEMS NOT FIXED (with reason):
  ⚠️  [FILE:LINE] — [why this wasn't fixed]

READY FOR RE-REVIEW: yes | no
  [If no — explain what's still outstanding]
```

---

## Rules

- Fix the review's intent, not just its literal suggestion
- One fix per issue — don't bundle unrelated changes
- If a suggested fix seems wrong, explain why and propose an alternative before implementing
- Never mark an issue as fixed without actually changing the code
