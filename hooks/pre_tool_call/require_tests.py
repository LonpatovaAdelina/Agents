#!/usr/bin/env python3
"""
Hook: require_tests
Trigger: PreToolCall on Write / Edit / MultiEdit
Purpose: Warn the agent when it writes implementation code without a corresponding test file.

Does NOT block — exits 0 always, but prints a warning that appears in the agent's context.
The agent is expected to act on the warning before completing the task.
"""

import json
import os
import sys

# Source directories where implementation code lives
SRC_DIRS = ["src/", "app/", "lib/"]

# File suffixes that indicate implementation (not tests, not config)
IMPL_SUFFIXES = [".ts", ".tsx", ".py", ".js", ".jsx"]

# Test file naming conventions to look for
TEST_PATTERNS = [
    "{stem}.test{ext}",
    "{stem}.spec{ext}",
    "{stem}_test{ext}",
    "test_{stem}{ext}",
]

# Directories where tests typically live
TEST_DIRS = ["tests/", "__tests__/", "test/", "spec/"]


def is_implementation_file(path: str) -> bool:
    """Returns True if path looks like a source implementation file."""
    for src_dir in SRC_DIRS:
        if path.startswith(src_dir) or f"/{src_dir}" in path:
            for suffix in IMPL_SUFFIXES:
                if path.endswith(suffix):
                    # Exclude already-test files
                    basename = os.path.basename(path)
                    if not any(
                        marker in basename
                        for marker in [".test.", ".spec.", "_test.", "test_"]
                    ):
                        return True
    return False


def find_test_file(path: str) -> str | None:
    """Try to locate an existing test file for the given implementation path."""
    basename = os.path.basename(path)
    stem, ext = os.path.splitext(basename)
    dir_path = os.path.dirname(path)

    # Check co-located test file (same directory)
    for pattern in TEST_PATTERNS:
        candidate = os.path.join(dir_path, pattern.format(stem=stem, ext=ext))
        if os.path.exists(candidate):
            return candidate

    # Check dedicated test directories
    for test_dir in TEST_DIRS:
        for pattern in TEST_PATTERNS:
            candidate = os.path.join(test_dir, pattern.format(stem=stem, ext=ext))
            if os.path.exists(candidate):
                return candidate

    return None


def main():
    try:
        tool_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = tool_input.get("tool_name", "")
    tool_params = tool_input.get("tool_input", {})

    if tool_name not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)

    path = tool_params.get("path", "")

    if not is_implementation_file(path):
        sys.exit(0)

    test_file = find_test_file(path)

    if test_file is None:
        basename = os.path.basename(path)
        stem, ext = os.path.splitext(basename)
        expected = f"{stem}.test{ext}"

        print(
            f"⚠️  WARNING [require_tests]: Writing to '{path}' but no test file found.\n"
            f"   Expected: '{os.path.dirname(path)}/{expected}' (or in a tests/ directory)\n"
            f"   Action required: Create the test file before marking this task complete.\n"
            f"   The test must cover: happy path, error cases, and edge cases for new behaviour.",
            file=sys.stderr,
        )
        # Exit 0 — warn but do not block. Agent must self-enforce.
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
