---
description: Gather requirements from the user and generate a Product Requirements Document (PRD)
argument-hint: [output-filename]
---

# Create PRD: Product Requirements Document Generator

## Overview

This instruction guides the agent through a **two-phase process**:
1. **Discovery** — gather product requirements through structured dialogue with the user
2. **Generation** — produce a complete `PRD.md` based on collected information

Output file: `$ARGUMENTS` (default: `PRD.md`)

---

## Phase 1: Discovery (Requirements Gathering)

Before writing anything, the agent must understand the product deeply.

### Step 1 — Initial Read
Review the full conversation history. Extract:
- Product idea / concept
- Any mentioned features, constraints, or goals
- Technical preferences or stack mentions
- Target audience hints

### Step 2 — Clarifying Questions
Ask the user **only the questions that remain unanswered** after reading the conversation. Group them logically and ask no more than **5–7 questions at once** to avoid overwhelming the user.

Use this question bank as a guide (adapt, skip, or add as needed):

**Product Identity**
- What problem does this product solve? Who has this problem?
- What makes this product different from existing solutions?
- What does success look like in 3 months after launch?

**Users**
- Who is the primary user? (role, technical skill level, context of use)
- Are there secondary user types (e.g. admins, API consumers)?

**Scope**
- What is the single most important feature for MVP?
- What features are explicitly out of scope for now?
- Are there hard deadlines or resource constraints?

**Technical**
- Is there a preferred tech stack or existing infrastructure to integrate with?
- What are the expected scale / load requirements?
- Any compliance, security, or data residency requirements?

**Integrations**
- Does the product need to connect to external services? (auth, payments, AI, etc.)
- Will there be a public API?

### Step 3 — Confirm Understanding
After gathering answers, provide a **1-paragraph summary** of your understanding and ask the user to confirm or correct before generating the PRD.

> Example: "Based on our conversation, I understand you're building X for Y users, with Z as the core MVP feature, using [stack]. The main constraint is [constraint]. Is this correct?"

---

## Phase 2: PRD Generation

Once requirements are confirmed, generate the PRD using the structure below.

### Writing Principles
- **Be specific** — avoid vague statements like "the app should be fast"; prefer "API responses < 200ms under normal load"
- **Be honest about unknowns** — mark assumptions explicitly with `[ASSUMED]`
- **Be scannable** — use headings, bullets, tables, checkboxes
- **Be consistent** — use the same terminology throughout

---

## PRD Structure

### 1. Header Block
```
Product: [Name]
Version: 0.1 (MVP Draft)
Status: Draft
Last Updated: [date]
Author: [agent/user]
```

---

### 2. Executive Summary
- What the product is (1 sentence)
- What problem it solves and for whom (1–2 sentences)
- Core value proposition
- MVP goal: what "done" looks like for v1

---

### 3. Problem Statement
- Current pain: what users struggle with today
- Root cause: why existing solutions fall short
- Impact: consequences of the problem remaining unsolved

---

### 4. Goals & Non-Goals

| Category | Item |
|----------|------|
| ✅ Goal | ... |
| ❌ Non-Goal | ... |

Keep this table tight — 5–8 items max per column.

---

### 5. Target Users

For each persona:
- **Name / Role**
- **Context:** when and how they use the product
- **Key needs:** top 3 things they need
- **Pain points:** what frustrates them today
- **Technical comfort:** beginner / intermediate / advanced

---

### 6. MVP Scope

#### In Scope ✅
Group by category (Core, Technical, Integrations, Deployment):
- ✅ Feature or requirement

#### Out of Scope ❌
- ❌ Feature deferred to future phases

---

### 7. User Stories

Format: `As a [persona], I want to [action], so that [outcome].`

Include:
- 5–8 primary stories covering the core loop
- 2–3 edge case or error state stories
- Acceptance criteria for each (bullet list)

---

### 8. Functional Requirements

Numbered list, grouped by feature area:

```
FR-01 [Feature Area]: [Requirement description]
FR-02 ...
```

Each requirement should be testable (avoid "should feel intuitive").

---

### 9. Non-Functional Requirements

| Requirement | Target | Priority |
|-------------|--------|----------|
| Performance | ... | High |
| Availability | ... | Medium |
| Security | ... | High |
| Scalability | ... | Low (MVP) |

---

### 10. Technical Preferences (input for architect)

Capture only what the user has explicitly stated — do not design, only record:
- Preferred languages or frameworks (if mentioned)
- Existing infrastructure to integrate with (if any)
- Hard constraints: budget, team skills, compliance requirements
- Scale expectations (rough order of magnitude)

> ⚠️ Full architecture, tech stack, and API spec are produced by the `architect` agent in `ARCHITECTURE.md` — do not design them here.

---

### 11. Security & Configuration

- Auth approach (e.g. JWT, OAuth, API keys)
- Secrets management
- Environment variables list (names only, no values)
- What's explicitly out of scope for security in MVP

---

### 12. Success Criteria

MVP is considered successful when:
- ✅ Functional criteria (what works)
- ✅ Quality criteria (performance, error rate)
- ✅ User criteria (can complete core task without help)

---

### 13. Implementation Phases (high-level only)

List 2–4 phases as **one sentence each** — no deliverables, no timelines. Detailed planning is handled by `plan-feature.md`.

Example:
- **Phase 1 — Foundation:** core data models, auth, project scaffold
- **Phase 2 — Core Features:** primary user-facing functionality
- **Phase 3 — Polish & Launch:** error handling, docs, deployment prep

> ⚠️ Detailed subtasks, file lists, and timelines are produced by `commands/core_piv_loop/plan-feature.md` — do not detail them here.

---

### 14. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |

Include 4–6 risks. Think about: technical debt, third-party dependencies, scope creep, team capacity.

---

### 15. Open Questions

List unresolved decisions that need input:
- [ ] Question or decision point
- [ ] ...

---

### 16. Future Considerations

Features and ideas intentionally deferred:
- Post-MVP enhancements
- Scaling strategies
- Integration opportunities
- Advanced features for later phases

---

### 17. Appendix (optional)

- Links to related documents, designs, or repos
- Glossary of terms
- Reference architecture examples

---

## Output Confirmation

After generating the PRD:
1. State the file path where it was written
2. List any `[ASSUMED]` items that need user validation
3. List any Open Questions that block progress
4. Suggest the immediate next step
5. **Update pipeline status:** set `status → "designing_architecture"` to signal `orchestrator` that `analyst` has completed and `architect` can proceed

---

## Agent Behavior Notes

- Do **not** skip Phase 1 if requirements are vague — always clarify first
- Do **not** invent features not discussed or implied by the user
- Do **not** ask all questions at once if only 2–3 are truly unknown
- **Do** flag contradictions in user requirements and ask for resolution
- **Do** mark every assumption with `[ASSUMED]` so the user can spot them quickly
- Sections with insufficient information should say: `⚠️ Needs clarification — see Open Questions`
