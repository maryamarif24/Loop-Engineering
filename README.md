# Loop Engineering: Projects Repository

This repository contains all 4 practice projects from the "Loop Engineering: A Crash Course" learning journey. Each project demonstrates a different concept of loop engineering, building from simple in-session loops to fully unattended scheduled loops.

## Overview

The course teaches loop engineering as the skill of designing systems that run on their own, moving from guiding every agent turn to designing loops with heartbeats, spines, maker-checker splits, and other components. Each project implements one or more concepts from the course.

## Projects Summary

### Project 1: In-Session Loop (Concept 4)
**Folder**: `loop-engineering-project1/`
- **Demonstrates**: In-session loops that run on a timer while you watch
- **Key concept**: Loop checks periodically; stops when task completes
- **What it does**: Polls for task completion (output file exists), reports when done
- **Heartbeat type**: In-session (stops when session closes)
- **Safety**: Success condition (file exists = done), manual cleanup possible
- **Python script**: `loop_engineering_project1.py` - demonstrates the loop pattern in Python

### Project 5: Full Morning Triage-to-PR Loop (Combining All Concepts)
**Folder**: `loop-engineering-project5/`
- **Demonstrates**: Integrated loop combining all concepts from Projects 1-4
- **Key concept**: Full morning triage-to-PR loop with spine memory across runs
- **What it does**: Combines in-session, conditional, scheduled with spine, and event-driven loops into one workflow
- **Heartbeat type**: Hybrid (scheduled 9am + event-driven between runs)
- **Safety**: Spine (progress.md) memory, max PRs per run, human gate, max tries cap
- **Python script**: `loop_engineering_project5.py` - demonstrates the full integrated loop in Python
- **Combines**: Project 1 (in-session) + Project 2 (conditional) + Project 3 (scheduled + spine) + Project 4 (event-driven)

### Project 2: Conditional Loop (Concept 5)
**Folder**: `loop-engineering-project2/`
- **Demonstrates**: Conditional loops (run-until-done) that stop when a condition becomes true
- **Key concept**: Loop runs until tests pass, with built-in safety caps
- **What it does**: Agent drafts fix → loop runs tests → checker decides PASS/FAIL → stops on PASS
- **Safety stops**: Success condition, limit (max tries), no-progress check
- **When to use**: Task ends and a command can prove the end condition
- **Python script**: `loop_engineering_project2.py` - demonstrates conditional loop in Python

### Project 3: Scheduled Loop with Spine (Concepts 6 + 12)
**Folder**: `loop-engineering-project3/`
- **Demonstrates**: Scheduled loops that run unattended on a clock, combined with spine memory
- **Key concept**: Loop runs every weekday at 9am; progress.md remembers between runs
- **What it does**: Every morning triages overnight CI failures, drafts fixes, reviewer checks, opens PRs for safe ones, flags risky ones for human decision
- **Heartbeat type**: Scheduled (runs even with laptop closed)
- **Spine**: progress.md - survives between runs, model forgets everything between runs
- **Safety**: Max 5 PRs per run, claude/* branch prefix, human gate for risky items
- **When to use**: Tasks that must run while you sleep (CI triage, dependency checks, daily summaries)
- **Python script**: `loop_engineering_project3.py` - demonstrates scheduled loop with spine in Python

### Project 4: Event-Driven "The Doorbell" (Concept 7)
**Folder**: `loop-engineering-project4/`
- **Demonstrates**: Event-driven loops that react when something happens (pull request opens)
- **Key concept**: Loop sits idle until an event triggers it, then runs and exits
- **What it does**: Listens for GitHub pull_request events, runs reviewer agent, posts PASS/FAIL review
- **Heartbeat type**: Event-driven (reacts when something arrives, no clock)
- **When to use**: PR reviews, issue triage, message responses, alert reactions
- **Python script**: `loop_engineering_project4.py` - demonstrates event-driven loop in Python

### Project 10: Retry Queue Loop (Concept 10)
**Folder**: `loop-engineering-project10/`
- **Demonstrates**: Priority-queue loops with retry logic that handles transient failures
- **Key concept**: Loop processes items by priority (high → medium → low), retries failures up to MAX_RETRIES, and remembers progress via spine (progress.md) between runs
- **What it does**: Sorts items by priority, processes in priority order with retry logic, caps items per run, updates spine with completed/failed state
- **Heartbeat type**: In-session (stops when task completes or max retries exhausted)
- **Safety**: Success condition, limit (max tries per item), no-progress check
- **Python script**: `loop_engineering_project10.py` - demonstrates retry queue loop in Python

### Project 11: Validation Queue Loop (Concept 13)
**Folder**: `loop-engineering-project11/`
- **Demonstrates**: Priority-queue loops with retry and validation logic that confirms processing correctness
- **Key concept**: Loop processes items by priority, retries failures, then validates processed results, and remembers spine state between runs
- **What it does**: Sorts items by priority, processes with retries, validates outcomes, tracks completed/failed/validated items in spine
- **Heartbeat type**: In-session (stops when task completes with validation)
- **Safety**: Success condition, limit (max tries per item), validation pass/fail check
- **Python script**: `loop_engineering_project11.py` - demonstrates validation queue loop in Python

### Project 12: Rate-Limited Queue Loop (Concept 14)
**Folder**: `loop-engineering-project12/`
- **Demonstrates**: Priority-queue loops with rate limiting (max items per run cycle) for sustainable pacing
- **Key concept**: Loop processes items by priority but caps processing at a set number per run cycle, resetting each new run to prevent burnout
- **What it does**: Sorts items by priority, processes up to rate limit per run, updates spine with completed state, rate limit resets each cycle
- **Heartbeat type**: In-session (stops when task completes or rate limit reached)
- **Safety**: Rate limit cap per run cycle, success condition, manual cleanup possible
- **Python script**: `loop_engineering_project12.py` - demonstrates rate-limited queue loop in Python

## Course Concepts Covered

| Project | Concept(s) | Key Learning |
|---------|-----------|--------------|
| 1 | 4 | In-session loops, timer while watching |
| 2 | 5 | Conditional loops, run-until-done, stop conditions |
| 3 | 6 + 12 | Scheduled loops, spine (memory between runs) |
| 4 | 7 | Event-driven loops, The Doorbell pattern |
| 10 | 10 | Retry queue loops, transient failure handling |
| 11 | 13 | Validation queue loops, processing + verification |
| 12 | 14 | Rate-limited queue loops, sustainable pacing |

## Core Loop Shape (All Projects)

Every loop in this repository follows the same six-part anatomy:

1. **Heartbeat** - What starts each beat (schedule, event, or timer)
2. **Worktree** - Isolation so parallel agents don't collide (Projects 3-4)
3. **Skill** - Project knowledge written once, loaded each run
4. **Subagents** - Maker-checker split (separate creator and reviewer)
5. **Connector** - MCP to act in real tools (open PRs, update tickets)
6. **Spine** - Memory file (progress.md) that survives between runs (Projects 3+)

## Running the Projects

Each project can be experienced conceptually by reading the `readme.md` file in its folder. For practical execution:

- **Project 1**: Demonstrates the simplest loop pattern - check → wait → check → wait → stop
  - Run: `python loop_engineering_project1.py`
- **Project 2**: Shows conditional loops with safety caps (max tries, no-progress check)
  - Run: `python loop_engineering_project2.py`
- **Project 3**: Requires setup of scheduled heartbeat (Claude Code Routines or OpenCode cron/GitHub Actions) and spine (progress.md)
  - Run: `python loop_engineering_project3.py`
- **Project 4**: Requires GitHub integration (opencode github install) and event triggers
  - Run: `python loop_engineering_project4.py`
- **Project 5**: Full morning triage-to-PR loop combining all concepts
  - Run: `python loop_engineering_project5.py`
- **Project 10**: Retry queue loop with retry logic and spine memory
  - Run: `python loop_engineering_project10.py`
- **Project 11**: Validation queue loop with retry and validation logic
  - Run: `python loop_engineering_project11.py`
- **Project 12**: Rate-limited queue loop with per-run caps for sustainable pacing
  - Run: `python loop_engineering_project12.py`

## Your Value in Loop Engineering

Across all projects, your value moves from:
- **Prompting** (guiding each agent turn) → **Looping** (designing the system that holds the steps)

You design the loop structure while the loop handles the repetitive steps in the middle. The two things you always own are:
- **Intent**: Stating what you want clearly enough that the result can be checked
- **Accountability**: Owning what ships

## Repository Structure

```
loop-engineering-project1/    # Project 1: In-Session Loop (Concept 4)
├── agents.md
├── readme.md
└── loop-files.md

loop-engineering-project2/    # Project 2: Conditional Loop (Concept 5)
├── agents.md
├── readme.md
└── loop-files.md

loop-engineering-project3/    # Project 3: Scheduled Loop (Concepts 6+12)
├── agents.md
├── readme.md
└── loop-files.md

loop-engineering-project4/    # Project 4: Event-Driven (Concept 7)
├── agents.md
└── readme.md

loop-engineering-project10/   # Project 10: Retry Queue Loop (Concept 10)
├── agents.md
├── loop-files.md
├── progress.md
└── readme.md
  loop_engineering_project10.py

loop-engineering-project11/   # Project 11: Validation Queue Loop (Concept 13)
├── agents.md
├── loop-files.md
├── progress.md
└── readme.md
  loop_engineering_project11.py

loop-engineering-project12/   # Project 12: Rate-Limited Queue Loop (Concept 14)
├── agents.md
├── loop-files.md
├── progress.md
└── readme.md
  loop_engineering_project12.py

README.md                     # This file - overview of all projects
```

## Next Steps

After completing Projects 1-5, you can:

1. **Deepen your understanding**: Review the "deeper notes" in the course (Parts 5-6, Routines appendix)
2. **Build more loops**: Practice projects 5-8 for increasing difficulty
3. **Explore Routines**: Configure cloud scheduled automations using the Routines appendix
4. **Graph engineering**: After this course, explore graph engineering for multiple looping systems
5. **Projects 10-12**: Practice retry, validation, and rate-limited loops for resilient and sustainable workflows

**Or restart the cycle**: Projects 1-5 cover the core loop engineering concepts; after completing all 5, you can restart with advanced practice, deeper notes, or build custom loops for your own use cases.

---

**Repository**: https://github.com/maryamarif24/Loop-Engineering.git
**Last updated**: All 12 projects from Loop Engineering: A Crash Course (Projects 10-12 added)