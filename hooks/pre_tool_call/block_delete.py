#!/usr/bin/env python3
"""
Hook: block_delete
Trigger: PreToolCall on Write / Edit / MultiEdit
Purpose: Prevent accidental deletion of critical project files.

Claude Code passes tool input via stdin as JSON.
Exit code 0 = allow, Exit code 2 = block (message shown to agent).
"""

import json
import sys

# Files that must never be deleted or overwritten with empty content
PROTECTED_FILES = {
    "AGENT.md",
    "SKILL.md",
    "create-prd.md",
    "PRD.md",
    "ARCHITECTURE.md",
    "README.md",
}

# Directories whose contents are protected from bulk deletion
PROTECTED_DIRS = {
    "skills/",
    "commands/",
    "hooks/",
}

# Minimum byte size — writing fewer bytes than this to a protected file is suspicious
MIN_PROTECTED_FILE_SIZE = 50


def is_protected_path(path: str) -> bool:
    filename = path.split("/")[-1]
    if filename in PROTECTED_FILES:
        return True
    for protected_dir in PROTECTED_DIRS:
        if path.startswith(protected_dir) or f"/{protected_dir}" in path:
            return True
    return False


def main():
    try:
        tool_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Can't parse input — allow and let the tool handle it
        sys.exit(0)

    tool_name = tool_input.get("tool_name", "")
    tool_params = tool_input.get("tool_input", {})

    # Check Write tool — catch empty or near-empty overwrites of protected files
    if tool_name == "Write":
        path = tool_params.get("path", "")
        content = tool_params.get("content", "")

        if is_protected_path(path) and len(content.encode()) < MIN_PROTECTED_FILE_SIZE:
            print(
                f"BLOCKED: Attempted to overwrite protected file '{path}' with "
                f"near-empty content ({len(content)} bytes). "
                f"Protected files cannot be truncated. "
                f"If you need to delete content, use Edit to remove specific sections.",
                file=sys.stderr,
            )
            sys.exit(2)

    # Check MultiEdit — catch operations that delete entire file contents
    if tool_name == "MultiEdit":
        path = tool_params.get("path", "")
        edits = tool_params.get("edits", [])

        if is_protected_path(path):
            for edit in edits:
                new_str = edit.get("new_str", "NONEMPTY")
                old_str = edit.get("old_str", "")
                # Replacing the entire file with nothing
                if new_str == "" and len(old_str) > 200:
                    print(
                        f"BLOCKED: Edit on '{path}' would delete a large section "
                        f"({len(old_str)} chars) with no replacement. "
                        f"This looks like an accidental deletion of a protected file.",
                        file=sys.stderr,
                    )
                    sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
