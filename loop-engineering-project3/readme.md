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

### Running the loop (Python)

This demonstrates the scheduled loop with spine using Python:

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project3.py
   ```
3. **Observe**: The script will:
   - Load progress.md spine (memory from previous runs)
   - Simulate morning CI triage (find overnight failures)
   - Draft fixes and invoke reviewer agent (maker-checker split)
   - Open PRs for safe fixes (PASS + low risk)
   - Flag risky/FAIL items to "needs a human" section
   - Save progress.md spine for tomorrow's run
   - Stop after one run (simulating scheduled 9am heartbeat)

**What happens**:
- Your value: Designing the loop structure (heartbeat, spine, maker-checker, connector)
- Loop's value: Finding work, drafting fixes, checking, and shipping safe PRs automatically
- Spine (progress.md) remembers between runs - tomorrow's run picks up where today stopped
- Max 5 PRs per run safety cap
- Human gate: Risky or FAIL items go to "needs a human" section

**To simulate multiple runs**: Run the script multiple times - each run reads the progress.md spine and picks up where the previous run stopped.

### Spine (progress.md) Format

The progress.md file survives between runs and serves as the loop's memory:

```
## Done
- 2026-06-22: fixed flaky test in test/auth (retry on token refresh)

## In progress
- Dependency audit: 3 of 7 advisories patched; lodash bump blocked by an API change

## Open / needs a human
- CVE-2026-xxxx in image lib — the fix changes the output format, escalating to a maintainer
```

### Safety Features Demonstrated

- **Max 5 PRs per run**: Loop stops after 5 PRs even if more candidates exist
- **claude/* branch prefix**: Only claude/* branches (simulated)
- **Success condition**: PASS + low risk (no API change, no data migration, no file deletion)
- **Human gate**: Risky or FAIL items → "needs a human" section - person decides later
- **Spine memory**: progress.md survives between runs; without it, loop repeats first step forever