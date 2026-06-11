#!/usr/bin/env python3
"""Manage Agent Collaboration Workflow task context files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TASKS_DIR = Path("docs/tasks")
TEMPLATES_DIR = Path("docs/templates")

PLACEHOLDER_RE = re.compile(r"(TODO\(|TODO:|TBD|FIXME|{{[^}]+}}|<[^>\n]+>)")

REQUIRED = {
    "context-pack.md": [
        "# Context Pack:",
        "## Task Summary",
        "## Source Links",
        "## Owner",
        "## Goals",
        "## Non-Goals",
        "## Assumptions",
        "## Constraints",
        "## Decisions",
        "## Validation Evidence",
        "## Known Risks",
        "## Current Status",
        "## Next Actions",
    ],
    "handoff.md": [
        "# Handoff:",
        "## Current State",
        "## Work Completed",
        "## Files Changed",
        "## Validation Run",
        "## Blockers",
        "## Open Questions",
        "## Next Safe Action",
    ],
    "pr-context-diff.md": [
        "# PR Context Diff:",
        "## Summary",
        "## Initial Context",
        "## Final Context",
        "## Changed Assumptions",
        "## Key Decisions",
        "## Validation Evidence",
        "## Risks And Follow-Ups",
        "## Reviewer Notes",
    ],
}


@dataclass
class Finding:
    severity: str
    path: Path
    message: str

    def format(self) -> str:
        return f"{self.severity}: {self.path}: {self.message}"


def repo_root() -> Path:
    return Path.cwd()


def task_dir(task_id: str) -> Path:
    return TASKS_DIR / task_id


def render_template(template_name: str, task_id: str, title: str, owner: str, source: str) -> str:
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise SystemExit(f"Missing template: {template_path}")
    text = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{TASK_ID}}": task_id,
        "{{TITLE}}": title,
        "{{OWNER}}": owner,
        "{{SOURCE}}": source,
    }
    for needle, value in replacements.items():
        text = text.replace(needle, value)
    return text


def write_if_missing(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def scaffold(args: argparse.Namespace) -> int:
    tid = normalize_task_id(args.task_id)
    created = []
    for name in REQUIRED:
        path = task_dir(tid) / name
        content = render_template(name, tid, args.title, args.owner, args.source)
        if write_if_missing(path, content):
            created.append(path)

    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    else:
        print(f"No files created. Task already exists: {task_dir(tid)}")
    return 0


def create_single(args: argparse.Namespace, filename: str) -> int:
    tid = normalize_task_id(args.task_id)
    title = args.title or tid
    owner = args.owner or "owner"
    source = args.source or "source"
    path = task_dir(tid) / filename
    content = render_template(filename, tid, title, owner, source)
    if write_if_missing(path, content):
        print(f"Created: {path}")
    else:
        print(f"Exists: {path}")
    return 0


def normalize_task_id(task_id: str) -> str:
    tid = task_id.strip()
    if not tid:
        raise SystemExit("Task id cannot be empty")
    if "/" in tid or "\\" in tid:
        raise SystemExit("Task id cannot contain path separators")
    return tid


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_file(path: Path, headings: list[str], strict: bool) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        findings.append(Finding("FAIL", path, "missing required file"))
        return findings

    text = read_text(path)
    for heading in headings:
        if heading not in text:
            findings.append(Finding("FAIL", path, f"missing required heading: {heading}"))

    if strict:
        for match in PLACEHOLDER_RE.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(Finding("FAIL", path, f"placeholder remains on line {line}: {match.group(0)}"))

    return findings


def check_task(task_id: str, strict: bool) -> list[Finding]:
    tid = normalize_task_id(task_id)
    base = task_dir(tid)
    findings: list[Finding] = []
    if not base.exists():
        return [Finding("FAIL", base, "missing task directory")]
    for filename, headings in REQUIRED.items():
        findings.extend(check_file(base / filename, headings, strict))
    return findings


def command_check(args: argparse.Namespace) -> int:
    findings = check_task(args.task_id, args.strict)
    if findings:
        for finding in findings:
            print(finding.format())
        return 1
    print(f"PASS: {task_dir(normalize_task_id(args.task_id))}")
    return 0


def discover_tasks() -> list[str]:
    if not TASKS_DIR.exists():
        return []
    return sorted(path.name for path in TASKS_DIR.iterdir() if path.is_dir())


def command_check_all(args: argparse.Namespace) -> int:
    tasks = discover_tasks()
    if not tasks:
        print(f"FAIL: {TASKS_DIR}: no task directories found")
        return 1

    all_findings: list[Finding] = []
    for tid in tasks:
        all_findings.extend(check_task(tid, args.strict))

    if all_findings:
        for finding in all_findings:
            print(finding.format())
        print(f"Checked tasks: {len(tasks)}")
        return 1

    print("PASS")
    print(f"Checked tasks: {len(tasks)}")
    for tid in tasks:
        print(f"- {tid}")
    return 0


def command_status(_: argparse.Namespace) -> int:
    tasks = discover_tasks()
    print(f"Tasks directory: {TASKS_DIR}")
    print(f"Task count: {len(tasks)}")
    for tid in tasks:
        findings = check_task(tid, strict=False)
        status = "ok" if not findings else "incomplete"
        print(f"- {tid}: {status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scaffold", help="Create all context files for a task")
    p.add_argument("task_id")
    p.add_argument("--title", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--source", required=True)
    p.set_defaults(func=scaffold)

    p = sub.add_parser("handoff", help="Create handoff.md for a task")
    p.add_argument("task_id")
    p.add_argument("--title")
    p.add_argument("--owner")
    p.add_argument("--source")
    p.set_defaults(func=lambda args: create_single(args, "handoff.md"))

    p = sub.add_parser("pr-diff", help="Create pr-context-diff.md for a task")
    p.add_argument("task_id")
    p.add_argument("--title")
    p.add_argument("--owner")
    p.add_argument("--source")
    p.set_defaults(func=lambda args: create_single(args, "pr-context-diff.md"))

    p = sub.add_parser("check", help="Validate one task")
    p.add_argument("task_id")
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=command_check)

    p = sub.add_parser("check-all", help="Validate all tasks")
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=command_check_all)

    p = sub.add_parser("status", help="Show task context status")
    p.set_defaults(func=command_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
