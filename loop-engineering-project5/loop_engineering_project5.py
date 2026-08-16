import time
import os
import pathlib
import json
import random

PROGRESS_FILE = pathlib.Path("progress.md")
OUTPUT_FILE = pathlib.Path("output.txt")


def load_spine():
    """Load progress.md spine memory. Returns dict with Done, In progress, Open sections."""
    spine = {"Done": [], "In progress": [], "Open / needs a human": []}
    if PROGRESS_FILE.exists():
        content = PROGRESS_FILE.read_text()
        current_section = None
        for line in content.splitlines():
            line_stripped = line.strip()
            if line_stripped.startswith("## "):
                current_section = line_stripped[3:]
                if current_section not in spine:
                    spine[current_section] = []
            elif line_stripped and current_section and line_stripped.startswith("- "):
                task = line_stripped[2:].strip()
                spine[current_section].append(task)
    return spine


def save_spine(spine):
    """Save progress.md spine memory."""
    lines = []
    lines.append("## Done")
    for item in spine.get("Done", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## In progress")
    for item in spine.get("In progress", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## Open / needs a human")
    for item in spine.get("Open / needs a human", []):
        lines.append("- " + item)
    lines.append("")
    PROGRESS_FILE.write_text("\n".join(lines))


def simulate_long_running_task():
    """Simulate a long-running operation that creates output after a delay (Project 1 concept)."""
    print("[Task] Starting long-running operation...")
    time.sleep(3)  # Simulate 3 seconds of work
    OUTPUT_FILE.write_text("Task completed successfully!")
    print("[Task] Operation complete. Output file created.")


def check_completion():
    """Check if the output file exists (Project 1 success condition)."""
    return OUTPUT_FILE.exists()


def simulate_test_suite(tries, max_tries):
    """Simulate a test suite that passes after N attempts (Project 2 concept)."""
    print("[Task] Running tests (attempt " + str(tries) + " of " + str(max_tries) + ")...")
    if tries >= max_tries:
        print("[Task] [PASS] Tests PASSED")
        return True
    print("[Task] [FAIL] Tests FAILED - retrying...")
    return False


def simulate_reviewer_paSS():
    """Simulate reviewer agent grading the change (Project 4 concept)."""
    result = random.choice(["PASS", "FAIL"])
    if result == "PASS":
        print("[Reviewer] --> PASS: no issues found, code quality good")
    else:
        print("[Reviewer] --> FAIL: issues identified, needs fixes")
    return result


def run_conditional_loop(max_tries=8, pass_after=3):
    """Conditional loop (Project 2 concept): runs until condition met with safety caps."""
    print("[Loop] Starting conditional loop (run-until-done)...")
    tries = 0

    while tries < max_tries:
        tries += 1
        print("[Loop] Try #" + str(tries) + "/" + str(max_tries))

        test_passed = simulate_test_suite(tries, max_tries)

        if test_passed:
            print("[Loop] [PASS] Success condition met: tests PASS!")
            print("[Loop] Task is complete. Loop stopping.\n")
            return True

        time.sleep(1)  # wait before retry

    print("[Loop] [STOP] Max tries reached - loop stopping (safety cap)")
    print("[Loop] Safety limit hit. Task not complete within allowed attempts.\n")
    return False


def simulate_ci_triage(spine):
    """Simulate triaging overnight CI failures (Project 3 concept)."""
    print("[Task] Starting morning CI triage...")
    candidates = []

    done_items = spine.get("Done", [])
    in_progress = spine.get("In progress", [])
    open_items = spine.get("Open / needs a human", [])

    # Simulate finding CI failures overnight
    ci_failures = [
        "Fix flaky test in test/auth (token refresh)",
        "Bump lodash dependency (API change blocking)",
        "Fix type error in report.ts"
    ]

    for failure in ci_failures:
        if failure not in done_items and failure not in in_progress:
            candidates.append(failure)

    print("[Task] Found " + str(len(candidates)) + " CI failure candidate(s) needing attention")
    return candidates


def run_scheduled_loop_with_spine(spine, max_candidates=5):
    """Scheduled loop with spine (Project 3 concept): processes candidates, updates spine."""
    print("[Loop] Starting scheduled loop with spine...")
    total_prs_opened = 0

    # Read progress.md (spine) - what's done, what's open
    print("[Loop] Step 1: Read progress.md (spine memory)")

    # Find work - CI failures
    candidates = simulate_ci_triage(spine)
    if not candidates:
        print("[Loop] No new candidates found - all caught up")
        return total_prs_opened

    print("[Loop] Step 2: Processing candidates (max " + str(max_candidates) + " per run)")

    for i, task in enumerate(candidates):
        if i >= max_candidates:
            print("[Loop] Reached max " + str(max_candidates) + " PRs cap - stopping this run")
            break

        print("[Loop] Candidate #" + str(i + 1) + ": " + task)

        # Draft fix in isolated worktree
        print("[Loop] Drafting fix in isolated worktree...")

        # Send diff to reviewer agent (maker-checker split - Project 4 concept)
        review_result = simulate_reviewer_paSS()

        # Decision based on review result
        if review_result == "PASS":
            print("[Loop] [PASS] Would open PR")
            total_prs_opened += 1
            spine["Done"].append(task + " (PR opened, PASS)")
        else:
            print("[Loop] [FAIL] Writing to 'needs a human'")
            spine["Open / needs a human"].append(task + " (FAIL, needs human decision)")

        # Update progress.md (spine) after each candidate - survives between runs
        save_spine(spine)

    print("[Loop] Spine saved for tomorrow's run")
    return total_prs_opened


def simulate_github_event():
    """Simulate a GitHub pull_request event arriving (Project 4 concept)."""
    events = [
        {
            "action": "opened",
            "pull_request": {"number": 150, "title": "Fix auth token refresh bug"},
            "pull_request_id": 150,
            "head_branch": "claude/fix/auth-token",
            "base_branch": "main",
            "changed_files": ["auth.py", "test_auth.py"],
        },
    ]
    return random.choice(events)


def run_event_driven_loop():
    """Event-driven loop (Project 4 The Doorbell pattern): sits idle until event, runs, exits."""
    print("[Loop] Starting event-driven loop (The Doorbell)...")
    print("[Loop] Waiting for event... (loop is idle, no clock, no one watching)")

    # Wait for event (simulated)
    event = simulate_github_event()
    pr_number = event["pull_request"]["number"]
    pr_title = event["pull_request"]["title"]

    print("[Event] pull_request opened event detected!")
    print("[Event] PR #" + str(pr_number) + ": " + pr_title)

    # Loop fires fresh run
    print("[Loop] Loop fires fresh run - reacting to event")

    # Run reviewer
    review_result = simulate_reviewer_paSS()

    # Take action
    if review_result == "PASS":
        print("[Loop] [PASS] Posting review on PR")
        print("[Loop] Review: 'Great work! No issues found.'")
    else:
        print("[Loop] [FAIL] Posting review with reasons")
        print("[Loop] Review: 'Here are the issues found.'")

    # Loop exits - goes idle again until next event
    print("[Loop] Loop exits - goes idle until next event")
    print("[Loop] No clock running - loop is quiet between events")


def run_loop():
    """Full morning triage-to-PR loop (Project 5): combines all concepts from Projects 1-4."""
    print("=" * 70)
    print("Loop Engineering: Project 5 - Full Morning Triage-to-PR Loop")
    print("=" * 70)
    print()
    print("Concepts combined:")
    print("  - Project 1: In-Session Loop (check -> wait -> check -> wait -> stop)")
    print("  - Project 2: Conditional Loop (run-until-done with safety caps)")
    print("  - Project 3: Scheduled Loop with Spine (progress.md memory between runs)")
    print("  - Project 4: Event-Driven Loop (The Doorbell - react to events)")
    print()
    print("Integrated morning workflow:")
    print("  1. Scheduled heartbeat triggers at 9am (or run manually)")
    print("  2. Load progress.md spine (memory from previous mornings)")
    print("  3. Find overnight CI failures (conditional loop)")
    print("  4. Draft fixes in isolated worktrees")
    print("  5. Reviewer agent grades each fix (maker-checker split)")
    print("  6. Open PRs for safe PASS fixes, flag risky FAIL for human decision")
    print("  7. Update progress.md spine for tomorrow's run")
    print("  8. Loop exits - spine remembers for next scheduled run")
    print()

    # Load spine (memory from previous runs)
    spine = load_spine()
    print("[Loop] Loaded spine: " + str(len(spine.get("Done", []))) + " done, "
          + str(len(spine.get("In progress", []))) + " in progress, "
          + str(len(spine.get("Open / needs a human", []))) + " needing human decision")

    total_prs = 0

    try:
        # Phase 1: Scheduled loop with spine (Project 3)
        print("\n[Phase 1] Scheduled loop with spine (morning triage)...")
        total_prs += run_scheduled_loop_with_spine(spine, max_candidates=3)

        # Phase 2: Conditional loop for any remaining work (Project 2)
        print("\n[Phase 2] Conditional loop for remaining tests...")
        conditional_result = run_conditional_loop(max_tries=8, pass_after=3)

        # Phase 3: Event-driven check (Project 4) - simulate a PR event
        print("\n[Phase 3] Event-driven loop (The Doorbell - simulated PR event)...")
        run_event_driven_loop()

        # Phase 4: In-session check (Project 1) - verify output
        print("\n[Phase 4] In-session loop check...")
        simulate_long_running_task()
        if check_completion():
            print("[Loop] [PASS] Output file detected - task complete!")
        else:
            print("[Loop] [WAIT] Output file not yet created")

        # Save spine after complete workflow
        save_spine(spine)

        print("\n[Overall] Morning triage complete!")
        print("[Overall] PRs opened: " + str(total_prs))
        print("[Overall] Spine saved for tomorrow's run at 9am")
        print("[Overall] Loop exiting - progress.md remembers state for next run")

    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")
        save_spine(spine)


if __name__ == "__main__":
    run_loop()