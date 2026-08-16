# Loop Engineering: Project 7 - Loop Files

## progress.md

The spine file that survives between runs, tracking:
- Batch progress (items processed, items failed)
- Last run timestamp
- Individual item status (success/failure/recovered)

## Output

The console output showing the nested loop execution flow, including:
- Outer loop iteration over batch items
- Inner conditional loops with retries
- Error recovery actions and escalation decisions