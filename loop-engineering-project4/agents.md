# Agents

This project demonstrates event-driven loop engineering concepts using OpenCode with GitHub triggers.

## Key Agents

- **Event Listener**: The loop that waits for repository events (pull requests, issues, etc.)
- **Implementer**: Drafts fixes or responses when events occur
- **Reviewer**: Separate agent that grades changes when PRs are opened
- **Spine Keeper**: Reads/writes progress.md memory between runs