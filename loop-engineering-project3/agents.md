# Agents

This project demonstrates loop engineering concepts using OpenCode with scheduled execution.

## Key Agents

- **Morning Triage**: The main loop that runs on schedule (weekday mornings)
- **Implementer**: Drafts fixes in isolated worktrees
- **Reviewer**: Separate agent that grades diffes and replies PASS/FAIL
- **Spine Keeper**: Reads/writes progress.md memory between runs