# Project 3: Scheduled Loop (Morning Brief with Memory)

## Demonstration: Scheduled loop running unattended with spine memory

### The Task (morning triage loop)
A scheduled loop that runs every weekday at 9am, sorting through overnight CI failures and safely shipping fixes.

### The Loop Structure
```
1. Heartbeat: Every weekday at 9am (schedule triggers the beat)
2. Read progress.md (spine): What's done, what's open, what needs human
3. Find the work (max 5 candidates):
   - CI failures overnight since last progress.md entry
   - Open issues labelled "bug" or "maintenance"
   - New advisories from npm audit
4. For each candidate:
   - Draft fix in isolated worktree (claude/<short-slug> branch)
   - Send diff to reviewer agent (maker-checker split)
   - Reviewer replies PASS or FAIL with reasons
   - If PASS + low risk: open pull request, link the issue
   - If FAIL or risky: write to "needs a human" in progress.md, no PR
5. Update progress.md (spine):
   - Move finished items to "Done" with today's date
   - Save progress.md for tomorrow's run
6. Exit - tomorrow's run reads what you saved
```

### What This Demonstrates

- **Concept 6: Scheduled Loops** - Runs on clock, even with laptop closed
  - Like an alarm clock: rings whether or not you are home
  - Claude Code: `/schedule` or Routines on claude.ai
  - OpenCode: cron, Task Scheduler, or GitHub Actions

- **Concept 12: The Spine** - Memory between runs
  - Model forgets everything between runs
  - progress.md is the spine: records what's done, open, needs human
  - Tomorrow's run reads progress.md and picks up where yesterday stopped
  - Without spine: loop repeats first step forever

### Spine (progress.md) - The Memory File

The progress.md file survives between runs and serves as the loop's memory:

```
## Done
- 2026-06-22: fixed flaky test in test/auth (retry on token refresh)

## In progress
- Dependency audit: 3 of 7 advisories patched; lodash bump blocked by an API change

## Open / needs a human
- CVE-2026-xxxx in image lib — the fix changes the output format, escalating to a maintainer
```

### How the Spine Works Each Run

| Step | What Happens |
|------|-------------|
| **Start** | Run reads progress.md first |
| **Find work** | Gathers candidates, skips items already under "Done" |
| **Do work** | Drafts fixes, runs reviewer, ships safe PRs |
| **End** | Updates progress.md: moves to "Done", saves state |

### Safety Features

| Feature | Purpose |
|---------|---------|
| **Max 5 PRs per run** | Prevents too many concurrent PRs |
| **claude/* branch prefix** | Never change main directly; only claude/* branches |
| **Success condition** | PASS + low risk (no API change, no data migration, no file deletion) |
| **Human gate** | Risky or FAIL items → "needs a human" section, person decides later |
| **Limit** | Max tries per candidate; overall loop caps |
| **No-progress check** | Stops if agent repeats same action with same arguments |

### Running the Loop

**Claude Code Setup**:
- Create a Routine on claude.ai
- Set schedule: weekdays at 9am
- Save skill: daily-triage (holds the steps so prompt stays one line)
- Spine: progress.md committed to repo
- Connector: GitHub app for PR creation

**OpenCode Setup**:
- GitHub Actions workflow with cron: `0 9 * * 1-5`
- Save skill: daily-triage in .opencode/skills/
- Spine: progress.md committed to repo
- Connector: anomalyco/opencode/github Action for PR creation
- Heartbeat: cron trigger fires fresh run each weekday 9am

### What You Wake Up To

After the loop runs unattended overnight (while you sleep):

- **Two PRs** opened for safe fixes (PASS from reviewer, low risk)
- **One flagged item** in "needs a human" section (FAIL or risky change)
- **progress.md updated** with today's date and status changes
- **You typed nothing** - the loop handled everything from finding work to opening PRs
- **Read progress.md** at 9:30am to review what the loop did

The loop: found the work → drafted each fix → separate reviewer graded every one PASS or FAIL → shipped the safe two as PRs → refused the risky one → handed you only the one decision that needed a person.

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure. The scheduled heartbeat starts each beat automatically; the spine (progress.md) remembers between runs; the loop handles finding work, drafting fixes, checking, and shipping safe PRs. You only make the one call that needs a person at the human gate.

### When to Use Scheduled Loops

- ✅ Tasks that must run while you sleep (CI triage, dependency checks, daily summaries)
- ✅ Repetitive maintenance work (daily/weekly audits, status reports, etc.)
- ❌ Tasks you're actively watching (use in-session loop instead)
- ❌ Tasks that need immediate human reaction (use event-driven loop instead)

### Your Value in This Loop

- **Designed the loop structure**: heartbeat, spine, maker-checker, connector, stop conditions
- **Set the stop conditions**: success condition (PASS + low risk), limit (max 5 PRs), human gate (risky → needs human)
- **Defined the intent**: "sort overnight CI, ship safe fixes, flag risky ones for human decision"
- **Received the result**: Two PRs and one flagged item waiting in progress.md when you woke up

### Stop Condition Hierarchy

1. **Success condition**: PASS from reviewer + low risk (no public API change, no data migration, no file deletion)
2. **Limit**: Max 5 PRs per run, max tries per candidate
3. **Human gate**: Risky or FAIL items → "needs a human" - person decides later, no PR opened
4. **No-progress check**: Stops if agent repeats same action with same arguments
5. **Overall limit**: Loop caps total runs to prevent infinite scheduling