# Agents

This project demonstrates the integrated morning triage loop combining all loop engineering concepts.

## Key Agents

- **Morning Triage**: The main loop that runs on schedule (9am) or when triggered
- **Implementer**: Drafts fixes in isolated worktrees for each CI failure candidate
- **Reviewer**: Separate agent that grades every diff and replies PASS/FAIL with reasons
- **Spine Keeper**: Reads/writes progress.md memory between runs, survives across multiple mornings
- **Event Listener**: Waits for GitHub pull_request events when loop is idle between scheduled runs

## Agent Workflow (Integrated)

| Agent | Role | When Active |
|-------|------|-------------|
| **Morning Triage** | Orchestrates the full 4-phase workflow | Scheduled heartbeat (9am) or manual run |
| **Implementer** | Drafts fix in isolated worktree (claude/<branch>) | Phase 1 - scheduled loop with spine |
| **Reviewer** | Grades diff, replies PASS or FAIL with specific reasons | Phase 1 (scheduled), Phase 3 (event-driven) |
| **Spine Keeper** | Updates progress.md: moves to "Done", saves "needs human" items | After each candidate in Phase 1; end of all phases |
| **Event Listener** | Wakes loop when GitHub PR event arrives | Phase 3 - between scheduled runs, loop is idle |