# Loop Engineering: Project 2 - Conditional Loop (Run-Until-Done)

## Overview

This project demonstrates **Concept 5: Conditional Loops (Run-Until-Done)** from the Loop Engineering course.

### What was built

- **Task**: Fix failing tests in a test suite
- **Loop**: A conditional loop that runs and checks tests, stopping only when they pass
- **Result**: Loop stops automatically on first successful test run (with max tries safety cap)

### Concept 5: Conditional Loops (Run-Until-Done)

- Stops when a specific condition becomes true (tests pass)
- Does NOT run on a fixed timer - stops because work is complete
- **Key difference from in-session loops**: Condition determines stop, not clock
- Separate checker decides "done" - the agent that performed work should not approve its own result

### How this loop works

```
1. Agent drafts a fix for failing tests
2. Loop runs tests (npm test) 
3. Checker (separate agent/command) decides: PASS or FAIL
4. If PASS: Loop stops, work complete
5. If FAIL: Loop retries (capped max tries)
6. If no progress: Loop stops to prevent infinite retry
```

### Safety features included

- **Max tries cap**: Never loops forever (prevents token bills growing out of control)
- **No-progress check**: Stops if agent repeats same action with same arguments
- **Always cap the tries**: Every loop needs three stops (success condition, limit, no-progress)

### Running the loop

This demonstrates the conditional loop pattern:
- **Your value**: Designing the stop condition ("tests must pass")
- **Loop's value**: Repeatedly trying, checking, and stopping when condition met
- **Checker value**: Tests and linter prove the work is actually fine (command cannot convince itself)

### Stop Conditions (the three guards)

Every loop needs these three stops:

| Stop | What it is | Leave out... |
|------|-----------|-------------|
| **Success condition** | How the loop knows the task is done | Loop can't stop on purpose or be graded |
| **Limit** | Max tries, max minutes, or max spend | Goal uses up whole token budget |
| **No-progress check** | Catch when agent repeats same action | Loop spends whole limit repeating one mistake |