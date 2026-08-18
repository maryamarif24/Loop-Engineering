# Loop Engineering: Project 11 - Validation Queue Loop

## Overview

This project demonstrates **Concept 13: Validation Queue Loop** from the Loop Engineering course.

### What was built

- **Task**: Process a batch of items with priorities, handle failures with retries, and validate processed results
- **Loop**: A validation-queue-aware loop that processes items by priority, retries failed items, validates successful processing, and respects spine memory between runs
- **Result**: Items are processed in priority order (high → medium → low), failed items are retried up to a maximum number of attempts, validated items are marked as confirmed correct, and progress is remembered via the spine file

### Concept 13: Validation Queue Loops

- Items may fail processing transiently
- Loop retries failed items with backoff between attempts
- After processing, items undergo validation to confirm correctness
- Spine (progress.md) remembers completed items, failed items, validated items, and queue state between runs
- Structure: `check queue → sort by priority → process with retries → validate → update spine → wait → ...`
- Loop handles the retry and validation logic; you provide the intent ("process and verify items reliably") and priority rules

### How this loop worked

1. Loaded the item queue and priority assignments from spine (progress.md)
2. Identified which items were already processed, which previously failed, which were validated, and which remain in the queue
3. Sorted remaining items by priority (high → medium → low)
4. Processed items in priority order, retrying failures up to MAX_RETRIES times
5. Validated newly processed items to confirm correctness
6. Updated spine with newly completed (validated) items, failed items, and validated items
7. Waiting until next run, remembering progress via spine

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project11.py
   ```
3. **Observe**: The script will:
   - Load queue state from progress.md spine
   - Identify remaining items and their priorities
   - Sort items by priority level
   - Process items in priority order with retry logic (up to 3 retries per item)
   - Cap processing at max items per run
   - Validate each processed item (80% pass rate simulation)
   - Update progress.md with new queue state (completed + failed + validated)
   - Report retry and validation processing summary

**What happens**:
- Your value: Designing the priority rules, retry policy, and validation criteria
- Loop's value: Handling the priority sorting, ordered processing, retry logic, and validation automatically
- Progress is remembered between runs via the spine file

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the priority sorting, ordered processing, retry logic, and validation; you provide the intent, priority rules, and receive the processed and verified results in priority order with resilience to failures.