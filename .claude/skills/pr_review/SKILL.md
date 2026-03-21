---
skill: pr-review
version: 1.0
applies-to: reviewer
activates-when: task is "review pull request", "PR review", "code review", or "review changes before merge"
---

# PR Review Skill

## Domain Overview

Pull request review is the last quality gate before code enters the main branch. The domain is distinct from general code review because a PR review must balance thoroughness with speed, evaluate changes in context (not in isolation), and produce feedback that the author can act on without a conversation. A general-purpose agent will often give vague feedback, miss the big picture by focusing on style, or approve code with security or logic issues because the individual files look fine.

---

## Core Principles

**1. Read the PR description before reading the code.**
Understand what the author intended before evaluating what they built. A PR without a description is incomplete — flag it before reviewing. Violation: jumping straight into the diff without understanding the goal.

**2. Distinguish blocking from non-blocking feedback.**
Every comment must be labelled. Blocking issues must be resolved before merge. Non-blocking issues are suggestions the author can take or leave. Unlabelled feedback creates ambiguity about whether approval is withheld. Violation: leaving 10 comments with no indication of which ones block approval.

**3. Review the design before the details.**
If the approach is wrong, line-level feedback is wasted effort. First evaluate: does this change solve the right problem in the right way? Only after confirming the approach is sound, review the implementation. Violation: spending 30 minutes commenting on variable names in a function that should not exist.

**4. One concern per comment.**
Each comment addresses one specific issue. Bundling multiple concerns into a comment makes it unclear what "resolved" means. Violation: "This function is too long, also it doesn't handle nulls, and the naming is confusing."

**5. Comment on the code, not the author.**
Feedback describes what the code does and why it's a problem — never implies carelessness or incompetence. Violation: "This is obviously wrong" or "Why would you do it this way?"

**6. Approve with comments when comments are non-blocking.**
If all remaining comments are non-blocking (suggestions, nits), approve and leave the comments. Do not withhold approval to force the author to respond to optional suggestions. Violation: requesting changes for a nit-level comment on a comma.

**7. Check what's not in the diff.**
A PR that adds a new endpoint should also add auth middleware, validation, error handling, and a test. If these are absent from the diff, that is a blocking issue — even though "missing code" is invisible in a diff. Violation: approving a new API endpoint without checking if auth and tests are present.

---

## Procedural Knowledge

### PR Review Workflow

**Step 1 — Orientation (before opening any file)**
- Read the PR title and description
- Identify the linked issue or requirement (flag if missing)
- Note the scope: new feature, bug fix, refactor, dependency update, or infrastructure
- Check the size: if the PR exceeds ~400 lines of meaningful change (excluding generated files), flag it as too large to review effectively

**Step 2 — Design review (high-level)**
- Does this change match the stated intent?
- Is the approach consistent with `ARCHITECTURE.md` and existing patterns?
- Are there simpler alternatives that the author may not have considered?
- Does this change introduce new dependencies? Are they justified?

**Step 3 — Implementation review (file by file)**
Review in this order:
1. Schema / data model changes first — they have the widest impact
2. Service / business logic — the core of correctness
3. Route / controller layer — surface area exposed to users
4. Tests — do they actually test the behaviour, or just cover lines?
5. UI components last — lowest risk

**Step 4 — Cross-cutting checks (things not visible in a single file)**
- Auth: are new endpoints protected?
- Validation: is all external input validated?
- Error handling: are all failure paths handled?
- Tests: is new behaviour covered?
- Migrations: if schema changed, is migration present and safe?
- Environment variables: are new env vars documented?

**Step 5 — Write and categorise all comments, then submit once**
Do not submit comments incrementally. Collect all feedback, categorise it, then submit the full review in one pass. Incremental comments create noise and make it hard for the author to see the full picture.

### Comment Format

Every review comment must follow this format:

```
[BLOCKING] or [SUGGESTION] or [QUESTION] or [NIT]

[Clear description of the issue or question]

[Why it matters — one sentence]

[Optional: concrete suggestion or example]
```

**Label definitions:**
- `[BLOCKING]` — must be resolved before merge; approval withheld
- `[SUGGESTION]` — recommended change; author decides; does not block approval
- `[QUESTION]` — seeking clarification; may become blocking depending on answer
- `[NIT]` — minor style or wording preference; absolutely does not block

### PR Size Guidelines

| Lines changed | Assessment |
|--------------|------------|
| < 200 | Ideal — full review possible |
| 200–400 | Acceptable — focus review on high-risk areas |
| 400–800 | Flag as too large; request a split if possible |
| > 800 | Decline to review until split (except generated files, lockfiles) |

When counting, exclude: generated files, lockfiles (`package-lock.json`, `yarn.lock`), migration auto-generated output, and test snapshots.

---

## Patterns & Anti-Patterns

```
PATTERN: High-level comment for structural issues
Context: When the approach itself needs to change
✅ DO: Leave a top-level PR comment explaining the design concern before leaving line comments
❌ DON'T: Leave 15 line-level comments that collectively imply "rewrite this"
Reason: A single high-level comment is faster to read and easier to act on than inferring a rewrite from fragments
```

```
PATTERN: Praise what's done well
Context: All reviews
✅ DO: Note specific things that are well-implemented ("Nice use of the result type here")
❌ DON'T: Only leave negative comments
Reason: Feedback-only reviews create a negative signal; balanced reviews are more trusted and acted on
```

```
PATTERN: Request changes only for blocking issues
Context: Final review decision
✅ DO: Approve with non-blocking comments when all blockers are resolved
❌ DON'T: Request changes for suggestions or nits
Reason: "Request changes" signals the PR is not mergeable; using it for nits devalues the signal
```

```
PATTERN: Verify tests test behaviour, not implementation
Context: Reviewing test files
✅ DO: Check that tests assert observable outcomes (return values, side effects, state changes)
❌ DON'T: Accept tests that only verify a function was called (mock-heavy tests with no assertions on outcome)
Reason: Implementation tests break on refactor without catching regressions; behaviour tests survive refactor
```

---

## Integration Points

- **Feeds into:** `commands/валидация/code-review.md` (PR review is the human-facing version of code-review)
- **Depends on:** all domain skills (`frontend`, `backend`, `database`, `auth`) — cross-reference their review checklists for domain-specific checks
- **Conflicts with:** none
- **Reviewer focus:** this skill IS the reviewer skill — it defines the review process itself

---

## Review Checklist

### Before Starting
- [ ] PR has a description explaining what and why
- [ ] PR is linked to an issue or requirement
- [ ] PR size is within reviewable range (< 400 meaningful lines)
- [ ] Branch is up to date with main/develop

### Design
- [ ] Approach matches architectural patterns in `ARCHITECTURE.md`
- [ ] No new dependency added without justification
- [ ] No scope creep (PR does what it says, nothing more)
- [ ] Breaking changes are documented

### Implementation
- [ ] All new endpoints have auth middleware
- [ ] All external input is validated
- [ ] All error paths are handled and return appropriate status codes
- [ ] No hardcoded secrets, tokens, or environment-specific values
- [ ] No `console.log` / debug statements left in
- [ ] No commented-out code

### Tests
- [ ] New behaviour has test coverage
- [ ] Tests assert outcomes, not just that functions were called
- [ ] Edge cases (empty, null, max values) are tested
- [ ] Tests are independent (no shared mutable state between tests)

### Data
- [ ] If schema changed: migration is present
- [ ] Migration is safe for production (no lock-acquiring operations on large tables without `CONCURRENTLY`)
- [ ] New columns have appropriate constraints

### Final
- [ ] All comments are labelled (BLOCKING / SUGGESTION / QUESTION / NIT)
- [ ] At least one piece of positive feedback is included
- [ ] Approval decision matches comment severity (approve if only non-blocking remain)
