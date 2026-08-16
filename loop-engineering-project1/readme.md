# Loop Engineering: Project 1 - In-Session Loop

## Overview

This project demonstrates **Concept 4: In-Session Loops** from the Loop Engineering course.

### What was built

- **Task**: A long-running operation that creates output after a delay
- **Loop**: An in-session loop that polls periodically to check if the task completed
- **Result**: The loop detected completion without requiring constant terminal watching

### Concept 4: In-Session Loops

- Fire beats on a timer while you watch the session
- Stop when the session closes (cannot run while you sleep)
- Structure: `check → wait → check → wait → ...` until condition met
- Loop holds the repetitive checking step; you provide the intent ("keep checking until done")

### How this loop worked

1. Started a simulated long-running task
2. Loop checked periodically if the output file existed
3. Once detected, reported completion once
4. Loop stopped cleanly - no terminal watching required

### Running the loop (Python)

This demonstrates the simplest form of loop engineering using Python:

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project1.py
   ```
3. **Observe**: The script will:
   - Simulate a long-running task (5-second delay)
   - Create `output.txt` when complete
   - Poll periodically until the output file is detected
   - Report completion automatically

**What happens**:
- Your value: Designing the loop structure ("keep checking until done")
- Loop's value: Handling the repeated checking step automatically
- No terminal watching required - the loop manages the wait-check cycle

### Running the loop (Batch equivalent)

For reference, the original batch-based approach is documented in `loop-files.md`.

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the repetitive checking; you provide intent and receive the result.