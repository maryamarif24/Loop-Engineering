# Loop Engineering: Project 9 - Priority Queue Loop

## Overview

This project demonstrates **Concept 11: Priority-Queue Loops** from the Loop Engineering course.

### What was built

- **Task**: Process a batch of items with priorities, handling high-priority items first
- **Loop**: A priority-queue-aware loop that sorts items by priority level before processing, with spine memory for progress between runs
- **Result**: The loop processes items in priority order (high → low), respects spine state from previous runs, and caps concurrent processing

### Concept 11: Priority-Queue Loops

- Items arrive with priority levels (high, medium, low)
- Loop uses priority ordering to determine processing sequence
- Spine (progress.md) remembers completed items and queue state between runs
- Structure: `check queue → sort by priority → process high-priority first → update spine → wait → ...`
- Loop holds the priority ordering logic; you provide the intent ("process items by priority")

### How this loop worked

1. Loaded the item queue and priority assignments from spine (progress.md)
2. Identified which items were already processed and which remain in the queue
3. Sorted remaining items by priority (high → medium → low)
4. Processed items in priority order, respecting any caps per run
5. Updated spine with newly processed items and updated queue state
6. Waiting until next run, remembering progress via spine

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project9.py
   ```
3. **Observe**: The script will:
   - Load queue state from progress.md spine
   - Identify remaining items and their priorities
   - Sort items by priority level
   - Process items in priority order (high → medium → low)
   - Cap processing at max items per run
   - Update progress.md with new queue state
   - Report priority processing summary

**What happens**:
- Your value: Designing the priority rules and queue structure
- Loop's value: Handling the priority sorting and ordered processing automatically
- Progress is remembered between runs via the spine file

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the priority sorting and ordered processing; you provide the intent, priority rules, and receive the processed results in priority order.