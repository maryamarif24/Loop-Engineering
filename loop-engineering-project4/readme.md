# Loop Engineering: Project 4 - Event-Driven (The Doorbell)

## Overview

This project demonstrates **Concept 7: Event-Driven Loops** from the Loop Engineering course, specifically "The Doorbell" pattern.

### What was built

- **Task**: Loop that reacts when a pull request is opened in a repository
- **Loop**: An event-driven loop that sits idle until a PR opens, then runs, reviews, and either opens a review or waits
- **Result**: A review appears on a PR on a computer that is not yours, whether your laptop is open or shut

### Concept 7: Event-Driven Loops

- Reacts the moment something happens (a PR opens, a message lands, an alert arrives)
- Sits idle with no clock and no one watching
- Then something happens: a PR, a message, an alert
- The loop reacts the instant it arrives, each on its own route, then goes quiet again
- **Claude Code**: Uses Channels and GitHub triggers
- **OpenCode**: Uses GitHub Action events (pull_request, issues, /oc or /opencode comments)

### The Doorbell Pattern

```
1. Loop sits idle - no clock, no one watching (no heartbeat running)
2. Event triggers: PR opens on connected repository
3. Loop fires fresh run: opencode run with GitHub event context
4. Loop reads the PR: diff, changed files, issue references
5. Implementer drafts review or fix in isolated worktree
6. Reviewer agent grades the change (PASS/FAIL with reasons)
7. If PASS: post review comment on the PR
8. If FAIL: post review with specific reasons for improvements
9. Loop exits - goes idle again until next event
```

### How GitHub Event-Driven Loops Work

**OpenCode GitHub Action** (the standard approach):

```yaml
name: opencode-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
jobs:
  review:
    runs-on: ubuntu-latest
    permissions: { contents: read, pull-requests: read }
    steps:
      - uses: actions/checkout@v6
        with: { persist-credentials: false }
      - uses: anomalyco/opencode/github@latest
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          model: anthropic/claude-sonnet-5
          use_github_token: true
          prompt: |
            Review this pull request for bugs, quality issues, and security risks.
            Read the diff, check for test coverage, look for edge cases.
            Reply with PASS or FAIL and specific reasons.
            If PASS: post a positive review summary.
            If FAIL: list specific changes needed, file by file.
```

**Claude Code Channels** (alternative approach):
- Set up a Channel that listens for GitHub webhook events
- When a PR opens, the session fires and the loop runs
- Same prompt structure, runs in a cloud session

### Key Differences from Other Loop Types

| Feature | In-Session | Conditional | **Event-Driven** | Scheduled |
|---------|-----------|-------------|------------------|-----------|
| **What starts it** | You keep session open | Stop condition | **Repository event** | Clock/schedule |
| **While you sleep?** | No | No | **Yes** | Yes |
| **Timer running?** | Yes | No | **No** | Yes |
| **Idles between runs?** | No (session holds timer) | No (loop holds state) | **Yes** (between events) | No (fresh run each tick) |
| **Best for** | Monitoring deploys | Make tests pass | **PR reviews, issue triage** | Daily/weekly maintenance |

### The Spine (progress.md) - Optional Memory

Even event-driven loops can benefit from a progress.md spine to remember:
- Last PRs already reviewed (avoid reviewing same PR twice)
- Common issues found across events
- Pattern of failures to track

```
## Reviewed PRs

- #142: flaky auth test - reviewed and approved
- #143: type error in report.ts - reviewed, FAIL (needs fix)

## Patterns Found

- Flaky tests on token refresh - 3 occurrences this week
- Missing lint on new files - common pattern
```

### Safety Features for Event-Driven Loops

| Feature | Purpose |
|---------|---------|
| **PR type filters** | Only react to specific event types (opened, synchronize, reopened) |
| **No infinite loops** | Loop exits after one run, goes idle until next event |
| **Idempotent actions** | Safe to repeat - don't create duplicate reviews or comments |
| **Read-only by default** | Check permissions limited to read/pull-requests:read unless writes needed |
| **Human gate for writes** | If PR creation or edits needed, add human approval step |

### Running the loop (Python)

This demonstrates the event-driven loop (The Doorbell pattern) using Python:

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project4.py
   ```
3. **Observe**: The script will:
   - Start in idle state (no clock running, loop waiting for event)
   - Simulate a GitHub pull_request event arriving
   - Fire a fresh loop run to react to the event
   - Invoke reviewer agent to grade the change
   - Post PASS review or FAIL review with specific reasons
   - Update progress.md spine to track reviewed PRs
   - Exit back to idle state until next event
   - Can run repeatedly - each iteration simulates a new PR event

**What happens**:
- Your value: Designing what the loop does **when** an event arrives
- Loop's value: Holding the "react → grade → respond" cycle automatically
- The heartbeat is the event itself (PR opens), not a schedule you manage
- Idempotent actions - safe to repeat, don't create duplicate reviews
- Spine (progress.md) tracks reviewed PRs to avoid duplicates

**To run multiple events**: Run the script - it will process one event then wait for the next.
Press Ctrl-C to stop.

### Safety Features for Event-Driven Loops

- **No infinite loops**: Loop runs once per event, then exits (goes idle)
- **Idempotency check**: Track reviewed PRs in spine - don't react to same PR twice
- **Rate limits**: Respect reasonable limits - process one PR per event cycle
- **Read-only by default**: Simulated read-only operations unless writes needed
- **Human gate for writes**: If loop needed to create PRs, human approval step included
- **Progress.md spine**: Tracks reviewed PRs and failure patterns between runs