# Loop Engineering: Project 7 - Nested Loop with Error Recovery

## Overview

This project demonstrates **Concept 9: Nested Loops with Error Recovery** from the Loop Engineering course.

### What was built

- **Task**: Process a batch of items with an outer supervisory loop that monitors inner processing loops
- **Loop**: A nested loop structure where an outer loop oversees multiple inner loops, each with error recovery
- **Result**: The outer loop detects failures in inner loops, triggers recovery, and continues processing

### Concept 9: Nested Loops with Error Recovery

- Outer loop supervises inner loops (each can be a different loop type: conditional, scheduled, event-driven)
- Inner loops have their own success/failure conditions and recovery strategies
- Error recovery patterns: retry, fallback, escalate, skip
- Spine (progress.md) remembers state across both outer and inner loop runs
- Structure: `supervise → inner-loop → check result → recover/retry → continue → wait → ...`

### How this loop worked

1. Outer loop iterates over a batch of items
2. For each item, an inner loop runs (simulating a conditional/check loop)
3. If inner loop fails, error recovery is triggered (retry up to max tries)
4. If recovery succeeds, continue to next item; if not, escalate for human decision
5. Progress is remembered via spine (progress.md) between runs

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project7.py
   ```
3. **Observe**: The script will:
   - Start an outer supervisory loop over a batch of items
   - For each item, run an inner conditional loop
   - If the inner loop fails, trigger error recovery (retries)
   - Update progress.md with status after each item
   - Report final batch summary

**What happens**:
- Your value: Designing the nested loop structure and error recovery policies
- Loop's value: Handling the repetitive inner checks and recovery actions automatically
- Progress is remembered between runs via the spine file

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the repetitive checking and recovery; you provide intent, error policies, and receive the batch result.