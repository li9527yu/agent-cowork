# Agent Collaboration Skill

Use this skill when a task needs durable context shared between Codex, Claude, Cursor, CI, and humans.

## Workflow

1. Identify the active task id from the user request, branch name, issue, PR, or `docs/tasks/`.
2. Read `AGENTS.md` and `docs/ai-collaboration-sop.md` if present.
3. Read `docs/tasks/<task-id>/context-pack.md` if present.
4. Read `docs/tasks/<task-id>/handoff.md` if present.
5. If no task context exists and the user wants implementation work, create it with:

   ```bash
   python3 tools/agent-context.py scaffold <task-id> --title "Short title" --owner "Owner" --source "Issue or conversation link"
   ```

6. During work, update the Context Pack when goals, assumptions, constraints, decisions, validation evidence, or known risks change.
7. Before stopping, update Handoff.
8. Before review, update PR Context Diff.
9. Validate with:

   ```bash
   python3 tools/agent-context.py check <task-id> --strict
   ```

## Rules

- Do not invent product intent, validation results, decisions, stakeholder approvals, or user approvals.
- Use explicit `TODO(<owner>): ...` entries for unknowns.
- Keep evidence concrete and reproducible.
- Prefer small updates to context artifacts over large rewrites.
- Report missing sections precisely enough for the next agent or human to fix them.
