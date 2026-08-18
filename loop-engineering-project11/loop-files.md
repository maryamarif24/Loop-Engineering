# Loop Engineering: Project 11 - Loop Files

## progress.md

The spine file that survives between runs, tracking:
- High, Medium, Low priority items remaining in queue
- Completed items across multiple runs
- Failed items and retry state
- Validated items confirming correctness
- Processing order and priority assignments

## Output

The console output showing the validation queue execution flow, including:
- Item pool and priority assignments
- Priority sorting determination (high → medium → low)
- Processing order execution by priority level
- Retry attempts and outcomes for failed items
- Validation results (pass/fail) for processed items
- Capping at max items per run
- Summary of completed vs remaining vs failed vs validated items