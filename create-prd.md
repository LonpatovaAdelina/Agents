## create-prd – PRD Generator Rule

This rule describes how to generate a concrete Product Requirements Document (PRD) for a new product based on a natural-language user request (e.g., "create a note-taking app").

---

### Task

Take the user's product request from the current conversation.
Infer the core idea, audience, and constraints.
Generate a structured PRD that describes the concrete product to be built.
Save or update the PRD in the specified file.

---

### Inputs

**Natural-language request** in the current conversation, e.g.:
  - "Create a note-taking app for students."
  - "I need a small CRM for freelancers."
   **Contextual hints** (if present):
  - Target platform (web, mobile, desktop, API).
  - Tech stack, integrations, constraints.
  - Deadlines, scope level (MVP vs. full product).
   **Target file path** (if given); otherwise choose a sensible default `prd.md`.

---

### Output

A single markdown PRD document that:
  - Describes a **specific, concrete product** derived from the request.
  - Is structured and scannable.
  - Can be handed directly to designers/engineers as a starting point.

Recommended PRD sections to generate:

-  Overview
-  Problem Statement
-  Goals & Non-Goals
-  Users & Use Cases
-  Product Scope & Features
-  Core Architecture (of the product)
-  UX / UI & Flows
-  Dependencies & Risks
-  Metrics & Success Criteria
-  Release Plan
-  Open Questions / Assumptions

---

### Workflow

- **1. Understand the request**
  - Parse the last user message and recent context.
  - Clarify internally:
    - What kind of product is this? (e.g., note-taking app, booking system, dashboard).
    - Who is the primary audience?
    - What are the main problems this product solves?

- **2. Build a product concept**
  - Derive:
    - Product name and short one-sentence summary.
    - Primary and secondary user groups.
    - Core value proposition.

- **3. Define product structure**
  - Identify:
    - Main modules / features.
    - Key entities (e.g., Notes, Tags, Workspaces, Users).
    - High-level navigation / screen map (for UI products).

- **4. Generate the PRD**
  - Fill each PRD section with:
    - Clear prose.
    - Bullet lists for features and flows.
    - Explicit assumptions and open questions where information is missing.

- **5. Persist the PRD**
  - If the file does not exist, create it.
  - If it exists, either:
    - Append a new dated version, or
    - Replace existing content (depending on configuration or instruction).

---

### Tools / Features (How the Generator Works)

- **Request Analyzer**
  - Reads the user request and recent conversation.
  - Extracts:
    - Product type (app, API, tool, etc.).
    - Domain (education, productivity, finance, etc.).
    - Target users and usage context.
    - Explicit constraints (tech stack, platforms, integrations).

- **Product Model Builder**
  - Converts the request into an internal **product model** that includes:
    - `productName`
    - `tagline` / summary
    - `primaryUsers` / `secondaryUsers`
    - `keyProblems`
    - `coreFeatures` and `stretchFeatures`
    - `nonGoals`
    - `constraints` and `assumptions`
  - Infers reasonable defaults when the user is vague (e.g., basic auth, responsive UI, minimal analytics).

- **Feature & Structure Generator**
  - From the product model, generates:
    - List of concrete features grouped by area (e.g., Capture, Organize, Share).
    - Conceptual information architecture (entities and relationships).
    - Suggested screen list or modules:
      - For apps: main screens, settings, onboarding, admin.
      - For APIs: core endpoints and resources.

- **PRD Template Renderer**
  - Maps the product model into the PRD sections listed in **Output**.
  - Uses markdown headings, bullets, and numbered lists.
  - Adds explicit "Open Questions" for uncertain or ambiguous parts of the request.

- **File Writer**
  - Determines the final file path (requested vs. default).
  - Ensures directories exist (e.g., `prd/`).
  - Writes the generated PRD content in a single operation.
  - Avoids duplicating identical content on repeated runs.

---

### Core Architecture (Generator Program)

- **High-Level Overview**
  - The generator program is a pipeline with four main stages:
    1. Input & Context Collection
    2. Product Intent Modeling
    3. PRD Synthesis
    4. File Output

- **Components**
  - **InputCollector**
    - Reads the latest user request and recent conversation.
    - Normalizes text (removes noise, consolidates constraints).
  - **IntentEngine**
    - Identifies user roles, problems, and desired outcomes.
    - Classifies product type and domain.
    - Builds the internal product model.
  - **StructureEngine**
    - Expands the product model into:
      - Feature sets (MVP vs. later).
      - Entities and relationships.
      - High-level architecture notes (frontend, backend, storage, integrations).
  - **PrdFormatter**
    - Converts the structured model into markdown.
    - Ensures all required sections are present.
    - Adds TODOs and questions where data is missing.
  - **FileManager**
    - Resolves and validates the target path.
    - Reads existing content (if any) when appending versions.
    - Writes the final markdown.

- **Extensibility**
  - Allow configuration for:
    - Level of detail (brief vs. detailed PRD).
    - Section set (add/remove sections such as Legal, Compliance, Localization).
    - Naming conventions for PRD files.

- **Error Handling**
  - If no clear product idea can be inferred:
    - Generate a short explanation and suggested clarifying questions instead of a PRD.
  - If file operations fail:
    - Surface a clear error message rather than silently discarding the PRD.

---

### Quality Checklist

- PRD clearly describes a **concrete product**, not just a vague idea.
- All key sections in **Output** are present.
- Features are grouped logically and are tied to user problems.
- Core product architecture is sketched at a high level.
- Assumptions and open questions are explicitly listed.
- The PRD is written in clear, concise language suitable for designers and engineers.



