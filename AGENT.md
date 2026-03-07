# AGENT.md — Multi-Agent Application Generator

## Project Overview

This system is a **multi-agent pipeline** built on **LangChain / LangGraph** that takes a user's product idea and autonomously generates a complete, production-ready application — including architecture decisions, project structure, and working code.

---

## Agent Roles & Responsibilities

### 1. `orchestrator` — Master Coordinator
- Entry point for all user requests
- Decomposes the user request into subtasks
- Routes tasks to the appropriate specialist agents
- Tracks overall pipeline state
- Assembles final output from agent results
- Handles retries and error escalation

### 2. `analyst` — Requirements Agent
- Interviews the user to gather requirements (uses `create-prd.md` instruction)
- Asks clarifying questions (max 5–7 per round)
- Confirms understanding before proceeding
- Produces: `PRD.md`

### 3. `architect` — System Design Agent
- Reads `PRD.md` and designs the technical solution
- Chooses tech stack, project structure, API contracts
- Produces: `ARCHITECTURE.md`, directory tree, API spec

### 4. `coder` — Code Generation Agent
- Reads `ARCHITECTURE.md` and implements each module
- Generates working, runnable code
- Follows project conventions defined by `architect`
- Produces: source files per the agreed directory structure

### 5. `reviewer` — Quality Agent
- Reviews generated code for correctness, security, consistency
- Checks that code matches PRD requirements
- Returns structured feedback to `coder` if issues found
- Signs off when quality bar is met

### 6. `documenter` — Documentation Agent
- Generates `README.md`, inline comments, usage examples
- Writes setup instructions and environment variable docs
- Produces: `README.md`, `docs/` folder if needed

---

## Pipeline Flow

```
User Request
     │
     ▼
[orchestrator] ──── decomposes & routes
     │
     ▼
[analyst] ──── clarifying questions → PRD.md
     │
     ▼
[architect] ──── tech stack + structure → ARCHITECTURE.md
     │
     ▼
[coder] ──── generates source code
     │
     ▼
[reviewer] ──── review loop (max 3 iterations)
     │           │
     │     issues found → back to [coder]
     │
     ▼
[documenter] ──── README + docs
     │
     ▼
Final Output: complete application
```

---

## State Schema (LangGraph)

```python
class PipelineState(TypedDict):
    # Input
    user_request: str

    # Documents
    prd: str                        # PRD.md content
    architecture: str               # ARCHITECTURE.md content

    # Generated artifacts
    files: dict[str, str]           # path → file content
    readme: str

    # Control flow
    current_agent: str
    review_iterations: int          # max 3
    review_feedback: str | None
    status: Literal[
        "gathering_requirements",
        "designing_architecture",
        "generating_code",
        "reviewing",
        "documenting",
        "done",
        "error"
    ]

    # Errors
    errors: list[str]
```

---

## Agent Behavior Rules

### All Agents
- Read only the state fields relevant to your role
- Write only to your designated output fields
- Never modify another agent's output directly — raise feedback through `review_feedback`
- Log reasoning steps before taking action
- If blocked, set `status: "error"` with a clear message in `errors`

### `orchestrator`
- Never generates content — only routes and assembles
- Respects `review_iterations` limit — escalates to user if exceeded
- Final assembly only happens after `reviewer` sign-off

### `analyst`
- Never assumes requirements — always asks
- Marks all assumptions with `[ASSUMED]` in PRD
- Does not proceed to next stage without explicit user confirmation

### `architect`
- Tech stack must match constraints in PRD (budget, team skill, deadlines)
- Every architectural decision must include a rationale (1 sentence)
- Produces a flat directory tree before writing `ARCHITECTURE.md`

### `coder`
- One file at a time — do not batch unrelated modules
- Follow the exact file paths defined by `architect`
- Do not introduce dependencies not listed in the architecture
- Leave `# TODO:` comments for anything deferred by design

### `reviewer`
- Structured feedback format:
  ```
  FILE: path/to/file.py
  ISSUE: description of the problem
  SEVERITY: critical | major | minor
  SUGGESTION: what to do instead
  ```
- `critical` issues block sign-off; `minor` issues are noted but do not block
- After 3 review cycles, escalate to user with summary

### `documenter`
- README must include: purpose, setup, usage, environment variables, project structure
- Do not repeat what is already in code comments
- Write for the target user persona defined in PRD

---

## File Conventions

| File | Owner | Description |
|------|-------|-------------|
| `PRD.md` | analyst | Product requirements |
| `ARCHITECTURE.md` | architect | Technical design |
| `README.md` | documenter | Setup & usage |
| `src/` | coder | All application source code |
| `docs/` | documenter | Extended documentation (optional) |
| `AGENT.md` | — | This file. System meta-instructions |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| User request too vague | `analyst` asks clarifying questions before proceeding |
| Conflicting requirements in PRD | `architect` flags conflict, pauses, asks user to resolve |
| Code fails reviewer after 3 cycles | Escalate to user with diff of issues |
| Unknown dependency needed | `coder` flags in `errors`, `orchestrator` asks user |
| Agent produces empty output | `orchestrator` retries once, then sets `status: error` |

---

## Constraints & Limits

- **Review loop max:** 3 iterations before human escalation
- **Files per run:** no hard limit, but each file must be listed in `ARCHITECTURE.md` first
- **Assumptions:** always marked `[ASSUMED]` — user must validate before shipping
- **Out of scope for agents:** deployment, CI/CD setup, secret management (flagged in README instead)

---

## Adding New Agents

To extend the pipeline with a new specialist agent:

1. Define its role and output fields in `PipelineState`
2. Add it as a node in the LangGraph graph
3. Define routing logic in `orchestrator`
4. Document it in this file under **Agent Roles & Responsibilities**
5. Add its output file convention to the **File Conventions** table

---

## Quick Reference

```
User idea → analyst → PRD.md
PRD.md → architect → ARCHITECTURE.md
ARCHITECTURE.md → coder → src/
src/ → reviewer → feedback loop (max 3x)
src/ → documenter → README.md
All outputs → orchestrator → final delivery
```
