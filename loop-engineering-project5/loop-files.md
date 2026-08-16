# Project 5: Full Morning Triage-to-PR Loop

## Demonstration: Integrated loop combining all concepts from Projects 1-4

### The Task (full morning triage)

A complete morning workflow that combines all four loop engineering concepts:
- In-session monitoring (Project 1)
- Conditional run-until-done (Project 2)
- Scheduled loop with spine memory (Project 3)
- Event-driven "The Doorbell" (Project 4)

### The Integrated Loop Structure

```
1. Heartbeat: Scheduled 9am trigger (or manual run) OR event-driven wake
2. Read progress.md (spine): What's done, what's open, what needs human decision
3. Find work: CI failures overnight, using conditional loop with safety caps
4. For each candidate (max 3 per run):
   - Draft fix in isolated worktree (claude/<short-slug> branch)
   - Send diff to reviewer agent (maker-checker split)
   - Reviewer replies PASS or FAIL with reasons
   - If PASS + low risk: open pull request, link the issue
   - If FAIL or risky: write to "needs a human" in progress.md
5. Update progress.md (spine): Move finished items to "Done", save for tomorrow
6. Exit: Loop exits - tomorrow's run reads progress.md and picks up where stopped
7. Event-driven interleave: Loop sits idle between events, wakes on pull_request
8. In-session check: Final verification task completes with output file detection
```

### What This Demonstrates

| Concept | Source Project | Integration Point |
|---------|---------------|-------------------|
| **In-Session Loop** | Project 1 | Phase 4 - final task verification, poll until output file exists |
| **Conditional Loop** | Project 2 | Phase 2 - run-until-done test suite with max tries cap |
| **Scheduled Loop** | Project 3 | Phase 1 - 9am weekday heartbeat, progress.md spine memory |
| **Event-Driven** | Project 4 | Phase 3 - idle until GitHub pull_request, then react and exit |

### Spine (progress.md) - The Memory File

The progress.md file survives between runs and serves as the loop's cumulative memory:

```
## Done
- Fix flaky test in test/auth (token refresh) (PR opened, PASS)
- Bump lodash dependency (API change blocking) (PR opened, PASS)

## In progress
- Fix type error in report.ts (FAIL, needs human decision)

## Open / needs a human
- CVE-2026-xxxx in image lib — the fix changes the output format, escalating to a maintainer
```

### How the Spine Works Across Runs

| Run | What Happens |
|-----|-------------|
| **Run 1** (first morning) | Loads empty spine; finds 3 CI failures; 2 PASS → PRs opened, 1 FAIL → "needs human"; spine saved with 2 Done, 1 Open |
| **Run 2** (next morning) | Loads spine from Run 1; skips 2 Done items; finds new CI failures; adds to spine; cumulative growth |
| **Run 3+** | Continues accumulating: more Done items, evolving "needs human" decisions, pattern tracking |

### Safety Features

| Feature | Purpose |
|---------|---------|
| **Max 3 PRs per run** | Prevents too many concurrent PRs in a single morning |
| **Max 8 tries conditional cap** | Loop stops if tests don't pass after 8 attempts |
| **Human gate for FAIL/risky** | Items going to "needs a human" - person decides, no auto-PR |
| **Spine memory survival** | Without progress.md, loop repeats first step forever across days |
| **Idempotent actions** | Safe to repeat - don't create duplicate reviews or PRs |

### Running the Loop

**Manual Execution**:

```bash
cd loop-engineering-project5
python loop_engineering_project5.py
```

**What to Observe**:

1. **Phase 1**: Scheduled loop processes up to 3 CI failure candidates
   - Reviewer grades each; 2 may PASS → "PR opened"; 1 may FAIL → "needs a human"
   - progress.md spine updated after each candidate

2. **Phase 2**: Conditional loop retries tests
   - Runs until PASS or max 8 tries reached
   - Safety cap prevents infinite retry

3. **Phase 3**: Event-driven loop
   - Loop goes idle (no clock, no one watching)
   - Simulated GitHub PR event fires fresh run
   - Reviewer grades; PASS review posted; loop exits back to idle

4. **Phase 4**: In-session loop check
   - Task simulates delay, then creates output file
   - Loop polls until output file exists
   - Reports "task complete" automatically

### Key Takeaway

Project 5 is the **full circle** of loop engineering. You design the structure that holds all four loop types in sequence, and the system handles the repetitive steps automatically. Your value is in defining the intent ("morning triage: sort CI, ship safe fixes, flag human decisions") and owning the result (PRs opened, decisions flagged in spine, spine updated for tomorrow).

### When to Use Project 5

- ✅ **Full practice**: Experience all 4 loop types in one workflow
- ✅ **Morning maintenance**: Continuous triage with spine memory across days
- ✅ **Concept integration**: See how in-session, conditional, scheduled, and event-driven loops work together
- ❌ **Just one concept** - use Projects 1-4 individually for focused learning