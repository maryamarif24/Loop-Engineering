# Loop Engineering: Project 10 - Retry Queue Loop

## Overview

This project demonstrates **Concept 10: Retry Queue Loop** from the Loop Engineering course.

### What was built

- **Task**: Process a batch of items with priorities, handling failures with retries and exponential backoff
- **Loop**: A retry-queue-aware loop that processes items by priority, retries failed items, and respects spine memory between runs
- **Result**: Items are processed in priority order (high → medium → low), failed items are retried up to a maximum number of attempts, and progress is remembered via the spine file

### Concept 10: Retry Queue Loops

- Items may fail processing transiently
- Loop retries failed items with backoff between attempts
- Spine (progress.md) remembers completed items, failed items, and queue state between runs
- Structure: `check queue → sort by priority → process with retries → update spine → wait → ...`
- Loop handles the retry logic; you provide the intent ("process items reliably") and priority rules

### How this loop worked

1. Loaded the item queue and priority assignments from spine (progress.md)
2. Identified which items were already processed, which previously failed, and which remain in the queue
3. Sorted remaining items by priority (high → medium → low)
4. Processed items in priority order, retrying failures up to MAX_RETRIES times
5. Updated spine with newly completed items and newly failed items
6. Waiting until next run, remembering progress via spine

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project10.py
   ```
3. **Observe**: The script will:
   - Load queue state from progress.md spine
   - Identify remaining items and their priorities
   - Sort items by priority level
   - Process items in priority order with retry logic (up to 3 retries per item)
   - Cap processing at max items per run
   - Update progress.md with new queue state (completed + failed)
   - Report retry processing summary

**What happens**:
- Your value: Designing the priority rules, retry policy, and queue structure
- Loop's value: Handling the priority sorting, ordered processing, and retry logic automatically
- Progress is remembered between runs via the spine file

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the priority sorting, ordered processing, and retry logic; you provide the intent, priority rules, and receive the processed results in priority order with resilience to failures.