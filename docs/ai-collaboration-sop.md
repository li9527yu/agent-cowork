# AI Collaboration SOP

This SOP defines how agents and humans preserve context across long-running work.

## Goals

- Make task state recoverable from the repository.
- Reduce repeated discovery when work moves between Codex, Claude, Cursor, CI, and humans.
- Keep review context close to the code.
- Separate verified evidence from assumptions.

## Core Artifacts

### Context Pack

Path:

```text
docs/tasks/<task-id>/context-pack.md
```

Purpose:

- Defines the task.
- Records goals, non-goals, assumptions, constraints, decisions, validation evidence, known risks, current status, and next actions.
- Should be updated whenever durable task understanding changes.

### Handoff

Path:

```text
docs/tasks/<task-id>/handoff.md
```

Purpose:

- Captures what changed in the current work session.
- Lists validation that was run.
- Identifies blockers and the next safe action.
- Should be updated before an agent or human stops work.

### PR Context Diff

Path:

```text
docs/tasks/<task-id>/pr-context-diff.md
```

Purpose:

- Explains the review-relevant change from initial context to final implementation.
- Records changed assumptions, tradeoffs, risks, validation, and review notes.
- Should be prepared before PR review.

## Agent Operating Rules

1. Start by identifying the active task id.
2. Read the Context Pack before making non-trivial changes.
3. Read the Handoff before resuming interrupted work.
4. Update context artifacts when durable facts change.
5. Record evidence as commands, outputs, links, screenshots, test reports, or review notes.
6. Do not fabricate validation evidence, product decisions, stakeholder approvals, or user intent.
7. Leave unknowns as explicit TODOs with an owner or question.
8. Run strict validation before handoff or PR.

## Validation Command

```bash
python3 tools/agent-context.py check-all --strict
```

## Suggested Adoption Order

1. Install this workflow.
2. Create one real task with `scaffold`.
3. Use the Context Pack during implementation.
4. Require Handoff before stopping work.
5. Require PR Context Diff for review.
6. Add scheduled automation only after the workflow is useful manually.
