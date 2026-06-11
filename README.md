# Agent Collaboration Workflow

A portable agent collaboration workflow for Codex, Claude, Cursor, and other coding agents.

This repository gives a project a shared way to preserve task context across agents:

- Context Pack: the durable task brief.
- Handoff: the current state for the next agent or human.
- PR Context Diff: review-focused summary of what changed and why.
- CLI checks: strict validation for missing files, missing sections, placeholders, and unfinished evidence.

The workflow is intentionally file-based so any tool can read it after cloning the project.

## Quick Install

Clone this repository, then run the installer from the target project you want to enable:

```bash
git clone https://github.com/YOUR_ORG/agent-collaboration-workflow.git
cd /path/to/your/project
/path/to/agent-collaboration-workflow/install.sh
```

Or pass the target path explicitly:

```bash
/path/to/agent-collaboration-workflow/install.sh /path/to/your/project
```

The installer adds:

```text
AGENTS.md
CLAUDE.md
.cursor/rules/agent-collaboration.mdc
.agents/skills/agent-collaboration/SKILL.md
docs/ai-collaboration-sop.md
docs/templates/context-pack.md
docs/templates/handoff.md
docs/templates/pr-context-diff.md
tools/agent-context.py
```

Existing `AGENTS.md` and `CLAUDE.md` files are not overwritten. The installer appends a managed include block instead.

## Create A Task

```bash
python3 tools/agent-context.py scaffold TASK-123 \
  --title "Short task title" \
  --owner "Owner or team" \
  --source "Issue, PR, ticket, or conversation link"
```

This creates:

```text
docs/tasks/TASK-123/context-pack.md
docs/tasks/TASK-123/handoff.md
docs/tasks/TASK-123/pr-context-diff.md
```

## Check Context Health

```bash
python3 tools/agent-context.py check-all --strict
```

Strict mode fails when required files or headings are missing, or when placeholders remain.

## Agent Prompts

### Codex Project Automation

Use this as a read-only scheduled project automation:

```text
Use $agent-collaboration.

Audit this project's agent collaboration context health.

Steps:
1. Read AGENTS.md and docs/ai-collaboration-sop.md if present.
2. Run `python3 tools/agent-context.py check-all --strict`.
3. If the command passes, report a short summary with the number of checked task context packs.
4. If the command fails, report each missing file, missing heading, placeholder, or escalated-task requirement exactly enough for a human or agent to fix it.
5. Do not modify files during this automation run unless the user explicitly asks for autofix.

Output format:
- Status: Pass / Fail
- Checked tasks:
- Findings:
- Recommended next action:
```

### Current Thread Heartbeat

Use this for a continuing thread:

```text
Use $agent-collaboration.

Continue the current agent collaboration workflow in this thread.

Each time this thread wakes up:
1. Identify the active task id from the thread context, branch name, issue link, or existing docs/tasks directory.
2. Read the task Context Pack and handoff if they exist.
3. Check whether recent work changed goals, assumptions, constraints, decisions, validation evidence, or known risks.
4. If the task is ready for review, ensure PR context diff content is prepared.
5. If context artifacts are missing or still contain placeholders, report the exact missing sections and ask for the minimum input needed.
6. Stop or ask for user input when no safe next action is available.

Output format:
- Current task:
- Context status:
- Work since last check:
- Missing information:
- Recommended next step:
```

## Recommended Workflow

1. Install the workflow into the target repository.
2. Ask an agent to read `AGENTS.md` or `CLAUDE.md`.
3. Create a task context pack with `python3 tools/agent-context.py scaffold ...`.
4. Keep `docs/tasks/<task-id>/context-pack.md` updated when goals, assumptions, constraints, decisions, risks, or validation evidence change.
5. Update `handoff.md` before stopping work.
6. Update `pr-context-diff.md` before review.
7. Run `python3 tools/agent-context.py check-all --strict` before handoff or PR.

## Repository Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── install.sh
├── docs/
│   ├── ai-collaboration-sop.md
│   └── templates/
├── skills/
│   └── agent-collaboration/
├── .agents/
│   └── skills/
├── .cursor/
│   └── rules/
└── tools/
    └── agent-context.py
```

## License

MIT
