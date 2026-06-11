# Agent Collaboration Workflow

This project uses file-based context artifacts so multiple agents and humans can continue work safely.

Before making substantial changes:

1. Read `docs/ai-collaboration-sop.md`.
2. Identify the active task id from the user's request, branch name, issue link, PR link, or `docs/tasks/`.
3. Read `docs/tasks/<task-id>/context-pack.md` if it exists.
4. Read `docs/tasks/<task-id>/handoff.md` if it exists.

During work:

- Keep goals, assumptions, constraints, decisions, validation evidence, and known risks current in the Context Pack.
- Do not invent product intent, validation results, stakeholder decisions, or user approvals.
- Mark unknowns as `TODO(<owner>): ...` with enough detail for follow-up.
- Preserve existing user changes unless explicitly asked to revert them.
- Prefer project scripts and documented commands over ad hoc replacements.

Before stopping:

1. Update `docs/tasks/<task-id>/handoff.md` with the current state, changed files, validation run, blockers, and next actions.
2. If preparing a PR, update `docs/tasks/<task-id>/pr-context-diff.md`.
3. Run `python3 tools/agent-context.py check <task-id> --strict` when the tool is available.

Useful commands:

```bash
python3 tools/agent-context.py scaffold TASK-123 --title "Short title" --owner "Owner" --source "Issue or PR link"
python3 tools/agent-context.py check TASK-123 --strict
python3 tools/agent-context.py check-all --strict
python3 tools/agent-context.py status
```
