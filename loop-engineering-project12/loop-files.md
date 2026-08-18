# Loop Engineering: Project 12 - Loop Files

## progress.md

The spine file that survives between runs, tracking:
- High, Medium, Low priority items remaining in queue
- Completed items across multiple runs
- Items processed in the current run cycle
- Processing order and priority assignments

## Output

The console output showing the rate-limited queue execution flow, including:
- Item pool and priority assignments
- Priority sorting determination (high → medium → low)
- Processing order execution by priority level
- Rate limit capping (max items per run cycle)
- Summary of completed vs remaining items per run cycle
- Note that rate limit resets each new run cycle