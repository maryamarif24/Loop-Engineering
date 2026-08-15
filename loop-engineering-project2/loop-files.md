# Project 2: Conditional Loop (Run-Until-Done)

## Demonstration: Loop making tests pass then stopping

### The Task (simulated)
A test fix scenario where the loop runs until tests pass, with safety caps.

### The Loop Structure
```
1. Agent drafts a fix for failing tests
2. Loop runs: npm test && npm run lint
3. Checker decides: PASS (tests green) or FAIL (errors remain)
4. If PASS: Loop stops - work complete
5. If FAIL: Loop retries (capped max tries)
6. If no progress: Loop stops to prevent infinite retry
```

### What This Demonstrates

- **Conditional loop** (Concept 5): Stops when condition is true, not on a timer
- "Run until the tests pass," not "run every five minutes while I watch"
- Separate checker decides "done" - agent should not approve its own result
- Loop holds the "try → check → retry" cycle automatically

### Safety Features

Three stops guard against failure:

| Stop | Purpose |
|------|---------|
| **Success condition** | `npm test -- test/auth && npm run lint` - proves work is done |
| **Limit** | Max tries cap - never loops forever (prevents token bills) |
| **No-progress check** | Detects stuck retry pattern - stops if same action repeats |

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the stopping condition. The loop handles the repeated trying and checking; you define what "done" means and set the safety limits.

### Stop Condition Hierarchy

This loop uses:
1. **Success condition**: Tests must actually pass (command cannot convince itself)
2. **Limit**: Max 8 tries - loop stops if condition never met
3. **No-progress check**: Stops if agent repeats same action with same arguments

### Cleanup

- Loop stops when tests pass OR max tries reached
- No files permanently modified (simulated fix scenario)
- Safety caps ensure loop cannot run indefinitely