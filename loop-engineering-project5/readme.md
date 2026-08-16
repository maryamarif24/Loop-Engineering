# Loop Engineering: Project 5 - Full Morning Triage-to-PR Loop

## Overview

This project demonstrates the **integrated morning triage workflow** combining all concepts from Projects 1-4. Project 5 is the full circle - from in-session monitoring through unattended scheduled loops with spine memory, to event-driven reactions and back.

**Concepts Combined**: Concepts 4 (In-Session), 5 (Conditional), 6+12 (Scheduled + Spine), and 7 (Event-Driven)

### What Was Built

- **Integrated Loop**: A complete morning workflow that combines all four loop types
- **Spine (progress.md)**: Memory file that survives between runs, enabling multi-day triage
- **Maker-Checker Split**: Separate reviewer agent grades every fix
- **Safety Caps**: Max tries, max PRs per run, human gate for risky changes
- **Unattended Execution**: Loop runs on schedule, even with laptop closed
- **Event-Driven Reactivity**: Loop responds to GitHub PR events between scheduled runs

## Running the Loop (Python)

### Prerequisites
- Python 3.x installed

### Steps to Run

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project5.py
   ```
3. **Observe**: The script will execute all four phases in sequence:
   - **Phase 1**: Scheduled loop with spine - triages CI failures, drafts fixes, reviewer checks, opens safe PRs
   - **Phase 2**: Conditional loop - runs tests until PASS with safety caps (max tries)
   - **Phase 3**: Event-driven loop - simulates GitHub PR event, runs reviewer, posts PASS/FAIL review
   - **Phase 4**: In-session loop - simulates task with delay, detects completion

### What Happens During Each Phase

| Phase | Concept | What It Does |
|-------|---------|-------------|
| **1** | Scheduled + Spine (Project 3) | Loads progress.md, finds CI failures, drafts fixes, invokes reviewer, opens PRs for PASS + low risk, flags FAIL/risky to "needs a human", saves spine for tomorrow |
| **2** | Conditional (Project 2) | Retries tests until PASS, capped at max tries; stops on success or safety limit |
| **3** | Event-Driven (Project 4) | Loop sits idle until PR event, then fires fresh run, reviews PR, posts PASS/FAIL review, exits back to idle |
| **4** | In-Session (Project 1) | Simulates long-running task, polls until output file exists, reports completion |

### Spine (progress.md) Format

The progress.md file survives between runs and serves as the loop's memory across days:

```
## Done
- Fix flaky test in test/auth (token refresh) (PR opened, PASS)
- Bump lodash dependency (API change blocking) (PR opened, PASS)

## In progress
- Fix type error in report.ts (FAIL, needs human decision)

## Open / needs a human
- CVE-2026-xxxx in image lib — the fix changes the output format, escalating to a maintainer
```

### Safety Features Demonstrated

- **Max 3 PRs per run**: Loop processes max 3 candidates even if more exist
- **Max tries cap**: Conditional loop stops after 8 attempts even if tests don't pass
- **Human gate**: FAIL or risky items go to "needs a human" section - person decides later, no PR opened
- **Spine memory**: progress.md persists between runs; without it, loop repeats first step forever
- **Idempotent actions**: Safe to repeat - don't create duplicate reviews or PRs
- **Three stop conditions every loop needs**: Success condition, limit, no-progress check

### Running Multiple Times

To simulate multiple mornings:
- Run the script multiple times
- Each run reads the progress.md spine and picks up where the previous run stopped
- "Done" items are skipped; new CI failures are found; spine accumulates history
- After 3+ runs, you'll see the spine grow with completed items and flagged decisions

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to **designing the loop structure** that holds all steps in the middle. Across all 5 projects, you:
- **Define the intent**: "Sort overnight CI, ship safe fixes, flag risky ones for human decision"
- **Design the structure**: Heartbeat, spine, maker-checker, connector, stop conditions
- **Receive the result**: Automated triage with PRs opened, decisions flagged, spine updated - all without constant terminal watching

### When to Use This Integrated Loop

- ✅ **Morning maintenance**: Triages overnight CI failures while you sleep
- ✅ **Full loop practice**: Experience all 4 loop types in one workflow
- ✅ **Multi-day tracking**: Spine remembers between runs for continuous improvement
- ❌ **Active monitoring** (watch terminal) - use Project 1 in-session loop instead
- ❌ **Simple test retry** - use Project 2 conditional loop alone
- ❌ **Scheduled maintenance only** - use Project 3 scheduled loop alone
- ❌ **Immediate PR reaction** - use Project 4 event-driven loop alone