#!/usr/bin/env python3
"""
Hook: save_context
Trigger: PreCompact
Purpose: Before Claude Code compacts the context window, snapshot the current
pipeline state so the agent can resume without losing track of where it was.

Writes: .context_snapshot.json in the project root.
The agent should read this file at the start of the next session (via prime.md).
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_file_safe(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return None


def extract_status_from_prd(content: str) -> str:
    """Try to extract Status field from PRD frontmatter or header block."""
    match = re.search(r"Status:\s*(.+)", content)
    return match.group(1).strip() if match else "unknown"


def extract_open_questions(content: str) -> list[str]:
    """Extract unchecked items from any Open Questions section."""
    match = re.search(r"##\s+Open Questions(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return []
    section = match.group(1)
    return re.findall(r"- \[ \] (.+)", section)


def extract_assumed_items(content: str) -> list[str]:
    """Find all [ASSUMED] markers in a document."""
    return re.findall(r"\[ASSUMED\][^\n]*", content)


def scan_todos(root: str = ".") -> list[dict]:
    """Walk src/ and find all # TODO: comments."""
    todos = []
    for dirpath, _, filenames in os.walk(root):
        # Skip hidden dirs and node_modules
        if any(part.startswith(".") or part == "node_modules" for part in dirpath.split(os.sep)):
            continue
        for filename in filenames:
            if not filename.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                lines = Path(filepath).read_text(encoding="utf-8").splitlines()
                for i, line in enumerate(lines, 1):
                    if "# TODO:" in line or "// TODO:" in line:
                        todos.append({"file": filepath, "line": i, "text": line.strip()})
            except Exception:
                continue
    return todos


def scan_stubs(root: str = ".") -> list[str]:
    """Find files containing [STUB] markers."""
    stubs = []
    for dirpath, _, filenames in os.walk(root):
        if any(part.startswith(".") or part == "node_modules" for part in dirpath.split(os.sep)):
            continue
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                content = Path(filepath).read_text(encoding="utf-8")
                if "[STUB]" in content:
                    stubs.append(filepath)
            except Exception:
                continue
    return stubs


def list_plans() -> list[dict]:
    """List plan files and their completion status."""
    plans = []
    plans_dir = Path("plans")
    if not plans_dir.exists():
        return plans
    for plan_file in sorted(plans_dir.glob("*.md")):
        content = plan_file.read_text(encoding="utf-8")
        total = len(re.findall(r"SUBTASK-\d+", content))
        # Heuristic: a subtask is "done" if all its checklist items are checked
        done = len(re.findall(r"- \[x\]", content, re.IGNORECASE))
        plans.append({
            "file": str(plan_file),
            "subtasks_total": total,
            "items_checked": done,
        })
    return plans


def main():
    snapshot = {
        "snapshot_at": datetime.now(timezone.utc).isoformat(),
        "trigger": "PreCompact",
        "pipeline": {},
        "documents": {},
        "code": {},
        "resume_hint": "",
    }

    # ── Document state ────────────────────────────────────────────────────────
    prd = read_file_safe("PRD.md")
    arch = read_file_safe("ARCHITECTURE.md")
    readme = read_file_safe("README.md")

    snapshot["documents"] = {
        "PRD.md": {
            "exists": prd is not None,
            "status": extract_status_from_prd(prd) if prd else None,
            "open_questions": extract_open_questions(prd) if prd else [],
            "assumed_items": extract_assumed_items(prd) if prd else [],
        },
        "ARCHITECTURE.md": {
            "exists": arch is not None,
            "open_questions": extract_open_questions(arch) if arch else [],
        },
        "README.md": {
            "exists": readme is not None,
        },
    }

    # ── Pipeline stage inference ──────────────────────────────────────────────
    if not prd:
        stage = "gathering_requirements"
    elif not arch:
        stage = "designing_architecture"
    elif not readme:
        stage = "generating_code_or_reviewing"
    else:
        stage = "documenting_or_done"

    snapshot["pipeline"]["inferred_stage"] = stage

    # ── Code state ────────────────────────────────────────────────────────────
    todos = scan_todos()
    stubs = scan_stubs()
    plans = list_plans()

    snapshot["code"] = {
        "todos": todos[:20],  # Cap at 20 to keep snapshot readable
        "todos_total": len(todos),
        "stubs": stubs,
        "plans": plans,
    }

    # ── Resume hint ──────────────────────────────────────────────────────────
    hints = []
    if not prd:
        hints.append("Run analyst: create-prd.md to gather requirements")
    elif extract_open_questions(prd):
        hints.append(f"PRD has {len(extract_open_questions(prd))} open question(s) — resolve before continuing")
    if stubs:
        hints.append(f"{len(stubs)} stub file(s) need implementation: {stubs[:3]}")
    if todos:
        hints.append(f"{len(todos)} TODO(s) remaining in code")
    if not hints:
        hints.append("Project appears complete — run system-review.md to verify")

    snapshot["resume_hint"] = " | ".join(hints)

    # ── Write snapshot ────────────────────────────────────────────────────────
    output_path = ".context_snapshot.json"
    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(
        f"📸 Context snapshot saved to '{output_path}'\n"
        f"   Stage: {stage}\n"
        f"   Resume hint: {snapshot['resume_hint']}\n"
        f"   Run 'prime.md' at the start of your next session to restore context.",
        file=sys.stderr,
    )

    sys.exit(0)


if __name__ == "__main__":
    main()
