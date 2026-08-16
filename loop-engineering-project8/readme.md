# Loop Engineering: Project 8 - Graph Loop

## Overview

This project demonstrates **Concept 10: Graph Loops** from the Loop Engineering course.

### What was built

- **Task**: Process interconnected items in a graph structure, where each item may depend on others
- **Loop**: A graph-aware loop that processes items respecting dependency edges, with spine memory for progress between runs
- **Result**: The loop processes items in correct order, handles cycles gracefully, and remembers state between runs

### Concept 10: Graph Loops

- Loops that operate on graph-structured data (items with dependencies)
- Topological sorting to determine processing order
- Cycle detection and breaking
- Spine (progress.md) remembers which items have been processed and which remain
- Structure: `check dependencies → process in order → update spine → wait → ...`
- Loop holds the graph traversal logic; you provide the intent ("process all reachable items")

### How this loop worked

1. Loaded the item dependency graph from spine (progress.md)
2. Detected which items were already processed and which are new
3. Used topological sort to determine processing order
4. Processed items respecting dependencies (item B waits for item A if A → B)
5. Updated spine with newly processed items
6. Waiting until next run, remembering progress

### Running the loop (Python)

**Prerequisites**: Python 3.x installed

**Steps to run**:

1. **Install**: Ensure Python is available (`python --version`)
2. **Run the script**:
   ```bash
   python loop_engineering_project8.py
   ```
3. **Observe**: The script will:
   - Load dependency graph from progress.md spine
   - Identify unprocessed items and their dependencies
   - Process items in correct topological order
   - Handle any cycles by breaking them gracefully
   - Update progress.md with new processing state
   - Report completion summary

**What happens**:
- Your value: Designing the graph structure and dependency rules
- Loop's value: Handling the complex traversal and ordering automatically
- Progress is remembered between runs via the spine file

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the graph traversal and dependency resolution; you provide the item graph and receive processed results.