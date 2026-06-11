# Claude Collaboration Instructions

This repository uses the Agent Collaboration Workflow.

Read these files before substantial work:

- `AGENTS.md`
- `docs/ai-collaboration-sop.md`
- `docs/tasks/<task-id>/context-pack.md`
- `docs/tasks/<task-id>/handoff.md`

Keep durable task context in files, not only in chat. If a task id is missing, infer it from the branch, issue, PR, or ask for the minimum required input.

Before ending a session, update the handoff and run:

```bash
python3 tools/agent-context.py check-all --strict
```

Do not fabricate validation evidence, decisions, or approvals. Use explicit TODOs for unknowns.
