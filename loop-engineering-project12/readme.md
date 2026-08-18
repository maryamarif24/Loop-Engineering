# Loop Engineering: Project 12 - Rate-Limited Queue Loop

## Overview

This project demonstrates **Concept 14: Rate-Limited Queue Loop** from the Loop Engineering course.

### What was built

- **Task**: Process a batch of items with priorities, respecting a rate limit (max items per run cycle)
- **Loop**: A rate-limited-queue-aware loop that processes items by priority (high → medium → low), caps processing at a maximum number of items per run cycle, and respects spine memory between runs
- **Result**: Items are processed in priority order, but the rate limit ensures sustainable processing speed across multiple runs, preventing burnout or resource exhaustion

### Concept 14: Rate-Limited Queue Loops

- Loops often need to process many items but at a sustainable pace
- Rate limiting (caps per run cycle) ensures the loop doesn't overwhelm systems or itself
- Spine (progress.md) remembers completed items and queue state between runs
- Structure: `check queue → sort by priority → process with rate cap → update spine → wait for next cycle → ...`
- Loop handles the rate enforcement; you provide the intent ("process sustainably") and priority rules

### How this loop worked

1. Loaded the item queue and priority assignments from spine (progress.md)
2. Identified which items were already completed and which remain in the queue
3. Sorted remaining items by priority (high → medium → low)
4. Processed items in priority order, capped at MAX items per run cycle (rate limit)
5. Updated spine with newly completed items and tracked this run's processing
6. Waiting until next run cycle, remembering progress via spine - the rate limit resets each new cycle

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project12.py
   ```
3. **Observe**: The script will:
   - Load queue state from progress.md spine
   - Identify remaining items and their priorities
   - Sort items by priority level
   - Process items in priority order, rate-limited to max 5 items per run cycle
   - Cap processing at max items per run
   - Update progress.md with new queue state
   - Report rate-limited processing summary

**What happens**:
- Your value: Designing the priority rules and rate limit policy
- Loop's value: Handling the priority sorting, ordered processing, and rate enforcement automatically
- Progress is remembered between runs via the spine file - rate limit resets each cycle

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the priority sorting, ordered processing, and rate enforcement; you provide the intent, priority rules, and rate limit, and receive the processed results in priority order with sustainable pacing across runs.