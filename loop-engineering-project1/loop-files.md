# Project 1: In-Session Loop

## Demonstration: Loop checking until task completes

### The Task (task-sleep.bat equivalent)
A simulated long-running operation that creates a file after completing.

### The Loop Structure
```
1. Check: Does the output file exist?
2. If NO: Wait (interval/timer)
3. If YES: Report completion, stop loop
4. Repeat steps 1-3 until condition met
```

### What This Demonstrates

- **In-session loop** (Concept 4): Runs on timer while session is open
- Loop holds the "check → wait" cycle automatically
- You designed the intent: "keep checking until done"
- Loop executed the repeated checks without you watching terminal

### Key Takeaway

Your value in loop engineering moves from guiding every agent turn to designing the loop structure that holds the steps in the middle. The loop handles the repetitive checking; you provide intent and receive the result.

### Stop Conditions

This loop uses a **success condition**: the output file existing proves the task is done. Without this check, the loop would keep running forever.

### Cleanup

- Loop can be stopped with Ctrl-C
- No files modified while loop was running (except the output file the task created)