# SKILL.md — How to Write Skills

## What Is a Skill?

A skill is a **modular, self-contained knowledge package** that extends `AGENT.md` by giving a specialist agent procedural expertise in a specific domain. Skills do not replace agents — they equip them.

Think of it this way:
- `AGENT.md` defines **who** the agents are and **how** they collaborate
- `commands/` defines **what actions** agents can take
- `skills/` defines **how to do things well** within a domain

A skill answers the question: *"What does an expert in this area know that a general-purpose model might get wrong?"*

---

## Skill File Structure

Every skill lives at `skills/[domain]/SKILL.md` and must follow this structure:

```
skills/
└── [domain]/
    └── SKILL.md       ← the skill file
```

If the skill needs supplementary reference material (patterns, snippets, checklists), add them as sibling files:

```
skills/
└── [domain]/
    ├── SKILL.md
    ├── patterns.md    ← optional: reusable patterns
    └── checklist.md   ← optional: review checklist
```

---

## Required Sections in Every Skill

### 1. Header Block
```
---
skill: [domain-name]
version: 1.0
applies-to: [which agent(s) use this skill]
activates-when: [condition that triggers loading this skill]
---
```

**`applies-to`** — which agent loads this skill (`coder`, `architect`, `reviewer`, or `all`)

**`activates-when`** — the condition that tells `orchestrator` to inject this skill into the agent's context. Examples:
- `PRD contains "React" or "frontend"`
- `task involves database schema changes`
- `feature requires user authentication`

---

### 2. Domain Overview (2–3 sentences)
What this domain is, why it's distinct, and what an agent without this skill would likely get wrong.

---

### 3. Core Principles
5–10 opinionated, specific rules that define quality in this domain.

**Good principle:** "Never store derived data — compute it from source of truth at read time unless performance profiling proves otherwise."

**Bad principle:** "Write clean code." (too vague, not actionable)

Each principle should include:
- The rule (one sentence)
- Why it matters (one sentence)
- What the violation looks like (one sentence)

---

### 4. Procedural Knowledge (the main body)
The "how to" content that a general-purpose model lacks. This is domain-specific and will vary by skill type. Structure it as step-by-step workflows, decision trees, or annotated patterns — whatever best captures the knowledge.

Organize by task type. Example for a `backend` skill:
- How to design an endpoint
- How to handle errors
- How to structure business logic
- How to write a migration

---

### 5. Patterns & Anti-Patterns
Concrete code-level (or design-level) examples of what to do and what to avoid.

Format:
```
PATTERN: [name]
Context: when to use this
✅ DO: [example or description]
❌ DON'T: [example or description]
Reason: [why the DO is better]
```

Aim for 4–8 patterns per skill.

---

### 6. Integration Points
How this skill interacts with other parts of the system:
- Which files this skill's output feeds into
- Which other skills this skill depends on or conflicts with
- What the `reviewer` agent should check specifically for this domain

---

### 7. Review Checklist
A concrete list of things the `reviewer` agent must verify for code produced under this skill. These become the domain-specific criteria inside `code-review.md`.

Format: yes/no checkable items, specific enough to be unambiguous.

---

## Skill Writing Principles

**Be opinionated.** A skill that says "you can use either X or Y" is not a skill — it's a glossary. Pick the approach and justify it.

**Be specific to your stack.** A `frontend` skill for a React + TypeScript project is different from one for Vue + JavaScript. Name the actual tools, libraries, and versions.

**Capture what models get wrong.** The most valuable content in a skill is the non-obvious stuff — common mistakes, subtle edge cases, decisions that look right but aren't.

**Stay procedural.** Skills are how-to guides, not reference docs. "Do X, then Y, then check Z" is better than "X is a concept that means..."

**Keep it scannable.** Agents read skills at the start of a task. Dense walls of text will be skimmed or ignored. Use headers, short paragraphs, and code examples.

---

## Skill Loading Protocol

The `orchestrator` is responsible for loading skills. It should:

1. Read the `activates-when` field of all available skills at session start
2. Match conditions against the current `PRD.md` and task description
3. Inject matching skill content into the target agent's context before the agent begins work
4. Log which skills were loaded in the `Prime Report` (see `commands/core_piv_loop/prime.md`)

An agent must not load its own skill — the orchestrator always decides.

---

## Available Skills

| Skill | Domain | Applies To | Location |
|-------|--------|-----------|----------|
| frontend | React UI components, styling, state | `coder`, `reviewer` | `skills/frontend/SKILL.md` |
| backend | API design, business logic, error handling | `coder`, `architect`, `reviewer` | `skills/backend/SKILL.md` |
| database | Schema design, migrations, query patterns | `architect`, `coder`, `reviewer` | `skills/database/SKILL.md` |
| auth | Authentication, authorization, session management | `coder`, `architect`, `reviewer` | `skills/auth/SKILL.md` |

---

## Adding a New Skill

1. Create `skills/[domain]/SKILL.md` following this structure
2. Fill all required sections — no empty sections allowed
3. Add the skill to the **Available Skills** table above
4. Define a precise `activates-when` condition — vague conditions cause skill over-loading
5. Add domain-specific checks to `commands/валидация/code-review.md` under a new section

---

## What a Skill Is NOT

- Not a tutorial or onboarding doc for humans
- Not a list of library documentation links
- Not a style guide (unless style directly affects correctness)
- Not a replacement for `ARCHITECTURE.md` — skills are reusable across projects, architecture is project-specific
