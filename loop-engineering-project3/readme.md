# Loop Engineering: Project 3 - Scheduled Loop (Morning Brief with Memory)

## Overview

This project demonstrates **Concept 6: Scheduled Loops (Unattended Schedules)** from the Loop Engineering course, combined with **Concept 12: The Spine (Memory Between Runs)**.

### What was built

- **Task**: Morning maintenance loop that sorts through overnight CI failures, drafts safe fixes, has them checked, opens PRs for safe ones, and flags the rest
- **Loop**: A scheduled loop that runs every weekday at 9am, using progress.md as the spine to remember between runs
- **Result**: You wake up to two PRs and one flagged decision - you typed nothing

### Concept 6: Scheduled Loops (Unattended Schedules)

- Runs on a clock, even with the laptop closed
- Like an alarm clock - rings whether or not you are home
- **Claude Code**: Uses `/schedule` or Routines on claude.ai
- **OpenCode**: Uses cron, Task Scheduler, or GitHub Actions
- Each tick launches a brand-new short-lived run, lets it finish, then shuts down

### Concept 12: The Spine (Memory Between Runs)

- Model forgets everything between runs
- Progress.md is the spine - records what's done, open, needs human
- Tomorrow's run reads progress.md and picks up where yesterday's run stopped
- **Without spine**: Loop repeats first step forever

### How This Loop Works

```
1. Heartbeat: Every weekday at 9am (schedule triggers the beat)
2. Read progress.md (spine): What's done, what's open, what needs human
3. Find the work: CI failures overnight, open issues, new audit advisories
4. For each candidate (max 5):
     - Draft fix in isolated worktree (worktree isolation)
     - Send diff to reviewer agent (maker-checker split)
     - If PASS and low risk: open pull request (connector/MCP)
     - If FAIL or risky: write to "needs a human" in progress.md
5. Update progress.md (spine): Move finished items to "Done", save for tomorrow
6. Exit - tomorrow's run reads what you saved
```

### Spine (progress.md) Format

```
## Done

- 2026-06-22: fixed flaky test in test/auth (retry on token refresh)

## In progress

- Dependency audit: 3 of 7 advisories patched; lodash bump blocked by an API change

## Open / needs a human

- CVE-2026-xxxx in image lib — the fix changes the output format, escalating to a maintainer
```

### Safety Features

| Feature | Purpose |
|---------|---------|
| **Max 5 PRs per run** | Prevents too many concurrent PRs |
| **claude/* branch prefix** | Never change main directly; only claude/* branches |
| **Success condition** | PASS + low risk (no API change, no data migration, no file deletion) |
| **Human gate** | Risky or FAIL items go to "needs a human" section, not PR |
| **Limit** | Max tries per candidate; loop caps overall runs |

### Running the Loop

**Claude Code**: Set up as a Routine on claude.ai, scheduled for weekday 9am

**OpenCode**: Set up as a GitHub Actions workflow with cron schedule:

```yaml
name: morning-maintenance
on:
  schedule:
    - cron: "0 9 * * 1-5"   # weekdays at 9am UTC
jobs:
  triage:
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write, issues: write }
    steps:
      - uses: actions/checkout@v6
        with: { persist-credentials: false }
      - uses: anomalyco/opencode/github@latest
        env: { ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }} }
        with:
          model: anthropic/claude-sonnet-5
          prompt: |
            Run the daily-triage skill.
            Read progress.md first; update it last.
            For each candidate fix: draft it on a new branch, then invoke the
            @reviewer subagent to grade it. Open a PR only when the reviewer
            replies PASS. Append anything risky to the "needs a human" section
            of progress.md and leave it for the maintainer.
```

### What You Wake Up To

After the loop runs unattended overnight:

- **Two PRs** opened for safe fixes (PASS from reviewer)
- **One flagged item** in "needs a human" section (FAIL or risky change)
- **You typed nothing** - the loop handled everything from finding work to opening PRs
- **Read progress.md** at human gate to review what the loop did

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure. The scheduled heartbeat starts each beat automatically; the spine (progress.md) remembers between runs; the loop handles finding work, drafting fixes, checking, and shipping safe PRs. You only make the one call that needs a person at the human gate.

### When to Use Scheduled Loops

- ✅ Tasks that must run while you sleep (CI triage, dependency checks, etc.)
- ✅ Repetitive maintenance work (daily/weekly summaries, audits, etc.)
- ❌ Tasks you're actively watching (use in-session loop instead)
- ❌ Tasks that need immediate human reaction (use event-driven loop instead)

### Your Value in This Loop

- **Designed the loop structure**: heartbeat, spine, maker-checker, connector
- **Set the stop conditions**: success condition, limit, human gate
- **Defined the intent**: "sort overnight CI, ship safe fixes, flag risky ones"
- **Received the result**: Two PRs and one flagged item waiting in progress.md

### Stop Conditions Hierarchy

1. **Success condition**: PASS from reviewer + low risk (no public API change, no data migration, no file deletion)
2. **Limit**: Max 5 PRs per run, max tries per candidate
3. **Human gate**: Risky or FAIL items go to "needs a human" - person decides later
4. **No-progress check**: Stops if agent repeats same action with same arguments