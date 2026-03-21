#!/usr/bin/env python3
"""
Hook: skill_eval
Trigger: PostToolCall on Write / Edit / MultiEdit
Purpose: Self-improvement loop for SKILL.md files.

When a SKILL.md is written or modified, this hook evaluates it against
binary assertions. If assertions fail, it writes a structured improvement
report that the agent can act on in the next iteration.

Inspired by the Karpathy-style eval loop:
  write change → run eval → pass? keep : rollback + report → repeat
"""

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ── Assertion definitions ────────────────────────────────────────────────────

@dataclass
class Assertion:
    id: str
    description: str
    blocking: bool  # True = must fix; False = warning only

    def check(self, content: str, path: str) -> tuple[bool, str]:
        """Returns (passed, failure_message)"""
        raise NotImplementedError


class HasRequiredSection(Assertion):
    def __init__(self, section_title: str, blocking: bool = True):
        super().__init__(
            id=f"has_section_{section_title.lower().replace(' ', '_')}",
            description=f"Must contain section: '{section_title}'",
            blocking=blocking,
        )
        self.section_title = section_title

    def check(self, content: str, path: str):
        if self.section_title.lower() in content.lower():
            return True, ""
        return False, f"Missing required section: '{self.section_title}'"


class HasFrontmatter(Assertion):
    def __init__(self):
        super().__init__("has_frontmatter", "Must have YAML frontmatter with skill, applies-to, activates-when", blocking=True)

    def check(self, content: str, path: str):
        required_keys = ["skill:", "applies-to:", "activates-when:"]
        if not content.startswith("---"):
            return False, "Missing YAML frontmatter block (must start with ---)"
        for key in required_keys:
            if key not in content:
                return False, f"Frontmatter missing required key: '{key}'"
        return True, ""


class MinPrincipleCount(Assertion):
    def __init__(self, minimum: int = 5):
        super().__init__(
            "min_principles",
            f"Core Principles section must have at least {minimum} numbered principles",
            blocking=True,
        )
        self.minimum = minimum

    def check(self, content: str, path: str):
        # Find Core Principles section
        match = re.search(r"##\s+Core Principles(.+?)(?=\n##|\Z)", content, re.DOTALL)
        if not match:
            return False, "Core Principles section not found"
        section = match.group(1)
        # Count bold-numbered principles: **1.**, **2.**, etc.
        count = len(re.findall(r"\*\*\d+\.", section))
        if count < self.minimum:
            return False, f"Core Principles has {count} principles (minimum {self.minimum})"
        return True, ""


class PrinciplesHaveViolation(Assertion):
    def __init__(self):
        super().__init__(
            "principles_have_violation",
            "Each principle must include a 'Violation:' example",
            blocking=True,
        )

    def check(self, content: str, path: str):
        match = re.search(r"##\s+Core Principles(.+?)(?=\n##|\Z)", content, re.DOTALL)
        if not match:
            return True, ""  # Can't check without section
        section = match.group(1)
        principle_count = len(re.findall(r"\*\*\d+\.", section))
        violation_count = len(re.findall(r"Violation:", section))
        if violation_count < principle_count:
            missing = principle_count - violation_count
            return False, f"{missing} principle(s) missing a 'Violation:' example"
        return True, ""


class HasPatterns(Assertion):
    def __init__(self, minimum: int = 3):
        super().__init__(
            "has_patterns",
            f"Must have at least {minimum} PATTERN blocks in Patterns & Anti-Patterns",
            blocking=True,
        )
        self.minimum = minimum

    def check(self, content: str, path: str):
        count = len(re.findall(r"```\nPATTERN:", content))
        if count < self.minimum:
            return False, f"Only {count} PATTERN blocks found (minimum {self.minimum})"
        return True, ""


class PatternHasAllFields(Assertion):
    def __init__(self):
        super().__init__(
            "pattern_has_fields",
            "Every PATTERN block must have Context, ✅ DO, ❌ DON'T, and Reason",
            blocking=True,
        )

    def check(self, content: str, path: str):
        patterns = re.findall(r"```\nPATTERN:.+?```", content, re.DOTALL)
        required_fields = ["Context:", "✅ DO:", "❌ DON'T:", "Reason:"]
        for i, pattern in enumerate(patterns, 1):
            for field in required_fields:
                if field not in pattern:
                    return False, f"PATTERN #{i} is missing field: '{field}'"
        return True, ""


class HasReviewChecklist(Assertion):
    def __init__(self, minimum_items: int = 8):
        super().__init__(
            "has_review_checklist",
            f"Review Checklist must have at least {minimum_items} checkbox items",
            blocking=True,
        )
        self.minimum_items = minimum_items

    def check(self, content: str, path: str):
        match = re.search(r"##\s+Review Checklist(.+?)(?=\n##|\Z)", content, re.DOTALL)
        if not match:
            return False, "Review Checklist section not found"
        section = match.group(1)
        items = re.findall(r"- \[[ x]\]", section)
        if len(items) < self.minimum_items:
            return False, f"Review Checklist has {len(items)} items (minimum {self.minimum_items})"
        return True, ""


class NoVagueLanguage(Assertion):
    VAGUE_PHRASES = [
        "write clean code",
        "be careful",
        "make sure to",
        "it is important",
        "best practices",
        "as appropriate",
        "when necessary",
        "if needed",
    ]

    def __init__(self):
        super().__init__(
            "no_vague_language",
            "Must not contain vague non-actionable phrases",
            blocking=False,  # Warning only
        )

    def check(self, content: str, path: str):
        content_lower = content.lower()
        found = [p for p in self.VAGUE_PHRASES if p in content_lower]
        if found:
            return False, f"Contains vague language: {found}. Replace with specific, actionable rules."
        return True, ""


class HasIntegrationPoints(Assertion):
    def __init__(self):
        super().__init__(
            "has_integration_points",
            "Must have an Integration Points section",
            blocking=False,
        )

    def check(self, content: str, path: str):
        if "## Integration Points" not in content:
            return False, "Missing 'Integration Points' section — add how this skill connects to other agents/skills"
        return True, ""


# ── Assertion registry ────────────────────────────────────────────────────────

SKILL_ASSERTIONS = [
    HasFrontmatter(),
    HasRequiredSection("Core Principles"),
    HasRequiredSection("Procedural Knowledge"),
    HasRequiredSection("Patterns & Anti-Patterns"),
    HasRequiredSection("Review Checklist"),
    MinPrincipleCount(minimum=5),
    PrinciplesHaveViolation(),
    HasPatterns(minimum=3),
    PatternHasAllFields(),
    HasReviewChecklist(minimum_items=8),
    NoVagueLanguage(),
    HasIntegrationPoints(),
]


# ── Eval runner ──────────────────────────────────────────────────────────────

def run_eval(content: str, path: str) -> dict:
    results = []
    for assertion in SKILL_ASSERTIONS:
        passed, message = assertion.check(content, path)
        results.append({
            "id": assertion.id,
            "description": assertion.description,
            "blocking": assertion.blocking,
            "passed": passed,
            "message": message,
        })
    return {
        "path": path,
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed_blocking": [r for r in results if not r["passed"] and r["blocking"]],
        "failed_warnings": [r for r in results if not r["passed"] and not r["blocking"]],
        "results": results,
    }


def write_eval_report(report: dict):
    """Write evaluation report to .skill_eval_report.json for the agent to read."""
    report_path = Path(report["path"]).parent / ".skill_eval_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    return report_path


def format_console_output(report: dict) -> str:
    lines = [
        f"\n{'='*60}",
        f"SKILL EVAL: {report['path']}",
        f"{'='*60}",
        f"Passed: {report['passed']} / {report['total']}",
    ]

    if report["failed_blocking"]:
        lines.append(f"\n🔴 BLOCKING FAILURES ({len(report['failed_blocking'])}) — must fix:")
        for f in report["failed_blocking"]:
            lines.append(f"  ✗ [{f['id']}] {f['message']}")

    if report["failed_warnings"]:
        lines.append(f"\n⚠️  WARNINGS ({len(report['failed_warnings'])}) — should fix:")
        for f in report["failed_warnings"]:
            lines.append(f"  ~ [{f['id']}] {f['message']}")

    if not report["failed_blocking"] and not report["failed_warnings"]:
        lines.append("\n✅ All assertions passed — skill is well-formed.")
    elif not report["failed_blocking"]:
        lines.append("\n✅ No blocking failures — skill can be used, but warnings remain.")
    else:
        lines.append(
            f"\n🔴 Skill has {len(report['failed_blocking'])} blocking issue(s). "
            "Fix and re-save to trigger re-evaluation."
        )

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    try:
        tool_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = tool_input.get("tool_name", "")
    tool_params = tool_input.get("tool_input", {})
    path = tool_params.get("path", "")

    # Only evaluate SKILL.md files
    if not path.endswith("SKILL.md"):
        sys.exit(0)

    if not os.path.exists(path):
        sys.exit(0)

    content = Path(path).read_text(encoding="utf-8")
    report = run_eval(content, path)
    report_path = write_eval_report(report)

    print(format_console_output(report), file=sys.stderr)

    if report["failed_blocking"]:
        print(
            f"\n📄 Full report saved to: {report_path}\n"
            f"   The agent should read this file and fix blocking issues before proceeding.",
            file=sys.stderr,
        )

    # Always exit 0 — eval reports don't block writes, they guide next iterations
    sys.exit(0)


if __name__ == "__main__":
    main()
