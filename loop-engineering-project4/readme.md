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

### Running the Loop

**OpenCode (GitHub Actions)**:
- Install once: `opencode github install` (adds .github/workflows/opencode.yml)
- The Action reacts to `pull_request` events automatically
- Each event fires a fresh opencode run inside GitHub Actions runner
- Reviewer prompt determines what the loop does each time

**Claude Code (Channels)**:
- Set up a Channel that connects to GitHub webhooks
- When PR opens, Claude Code session fires automatically
- Prompt runs review against the new PR
- Can close session after, or keep alive for more events

### What Happens When a PR Opens

1. **Event arrives**: `pull_request opened` on connected repo
2. **Loop fires**: Fresh opencode run starts in GitHub Actions
3. **Reads the PR**: Checks out code, reads diff, sees what changed
4. **Runs reviewer**: Invokes @reviewer subagent with the diff
5. **Reviewer replies**: `PASS` with what was verified, or `FAIL` with reasons
6. **Action taken**:
   - **PASS**: Post review "Great work! No issues found. :white_check_mark:"
   - **FAIL**: Post review "Here are the issues found:" with specific file:line reasons
7. **Loop exits**: Goes idle until next event
8. **You may never know**: Whether laptop was open or shut, the loop reacted

### Key Takeaway

Your value in event-driven loop engineering: designing what the loop does **when** an event arrives, not **how** to start it. The heartbeat is the event itself (PR opens), not a schedule you manage. The loop holds the "react → grade → respond" cycle automatically. You define the prompt/instructions for each event type.

### When to Use Event-Driven Loops

- ✅ **PR reviews**: Auto-review every PR that opens (this project)
- ✅ **Issue triage**: Auto-label, assign, or comment on new issues
- ✅ **Message responses**: Reply to Slack/Discord messages with templates
- ✅ **Alert responses**: React to CI failures, security alerts, monitoring alerts
- ❌ **Repetitive maintenance** (daily summaries) - use scheduled loop instead
- ❌ **Tasks you're actively watching** - use in-session loop instead

### Your Value in This Loop

- **Designed the event response**: What the loop does when PR opens, issue lands, etc.
- **Wrote the reviewer prompt**: Instructions for PASS/FAIL decisions
- **Set safety boundaries**: Read-only permissions, idempotent actions, no infinite loops
- **Received the result**: Auto-review posted on PRs whether you were at your computer or not

### Stop Conditions for Event-Driven

Event-driven loops have unique stop conditions since they run once per event:

1. **Natural stop**: Loop runs once per event, then exits (no infinite loop)
2. **Idempotency check**: Don't react to same event twice (track reviewed PRs in spine)
3. **Rate limits**: Respect GitHub API limits - don't flood with reviews
4. **Human gate for writes**: If loop needs to comment/edit PR, add human approval if risky

### Cleanup

- Loop exits after one event run, goes idle
- No files permanently modified unless reviewer suggests changes
- Spine (progress.md) can track reviewed PRs to avoid duplicates
- Loop is safe to leave running - it does nothing until an event arrives

---

**Projects 1-4 complete!**

- **Project 1**: In-session loop (checks while you watch, Concept 4)
- **Project 2**: Conditional loop (stops when condition met, Concept 5)
- **Project 3**: Scheduled loop (runs unattended, uses spine, Concept 6+12)
- **Project 4**: Event-driven (reacts to events, The Doorbell, Concept 7)

Ready for Project 5 (full morning triage-to-PR loop) or any concept review?