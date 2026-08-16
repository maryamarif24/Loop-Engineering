import time
import os
import pathlib
import json
import random

PROGRESS_FILE = pathlib.Path("progress.md")
EVENT_FILE = pathlib.Path("last_event.json")


def load_progress():
    """Load progress.md spine - tracks reviewed PRs to avoid duplicates."""
    spine = {"Reviewed PRs": [], "Patterns": []}
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
                item = line_stripped[2:].strip()
                spine[current_section].append(item)
    return spine


def save_progress(spine):
    """Save progress.md spine."""
    lines = []
    lines.append("## Reviewed PRs")
    for item in spine.get("Reviewed PRs", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## Patterns Found")
    for item in spine.get("Patterns", []):
        lines.append("- " + item)
    lines.append("")
    PROGRESS_FILE.write_text("\n".join(lines))


def simulate_github_event():
    """Simulate a GitHub pull_request event arriving."""
    events = [
        {
            "action": "opened",
            "pull_request": {"number": 145, "title": "Fix auth token refresh bug"},
            "pull_request_id": 145,
            "head_branch": "claude/fix/auth-token",
            "base_branch": "main",
            "changed_files": ["auth.py", "test_auth.py"],
        },
        {
            "action": "opened",
            "pull_request": {"number": 146, "title": "Update lodash dependency"},
            "pull_request_id": 146,
            "head_branch": "claude/fix/lodash-bump",
            "base_branch": "main",
            "changed_files": ["package.json", "lodash"],
        },
        {
            "action": "opened",
            "pull_request": {"number": 147, "title": "Refactor data service"},
            "pull_request_id": 147,
            "head_branch": "claude/fix/refactor-service",
            "base_branch": "main",
            "changed_files": ["data.service.ts", "utils.ts"],
        },
    ]
    import random
    return random.choice(events)


def simulate_reviewer(diff_summary):
    """Simulate separate reviewer agent grading the change."""
    print("[Reviewer] Analyzing diff...")
    # Simulate: 2 PASS, 1 FAIL
    result = random.choice(["PASS", "PASS", "FAIL"])
    if result == "PASS":
        print("[Reviewer] -> PASS: no issues found, code quality good")
        return "PASS", "No issues found."
    else:
        print("[Reviewer] -> FAIL: issues identified, needs fixes")
        reasons = [
            "Missing test coverage for edge cases",
            "Potential security vulnerability in input handling",
            "Type mismatch in API response",
        ]
        reason = random.choice(reasons)
        return "FAIL", reason


def run_loop():
    """Event-driven loop - The Doorbell pattern.

    Loop sits idle until a GitHub pull_request event arrives,
    then runs, reviews, posts review, and exits back to idle.
    """
    print("=" * 60)
    print("Loop Engineering: Project 4 - Event-Driven (The Doorbell)")
    print("=" * 60)
    print()

    spine = load_progress()
    print("[Loop] Loading spine (progress.md) - memory between events")
    print("[Loop] Spine tracks reviewed PRs to avoid duplicates")
    num_reviewed = len(spine.get("Reviewed PRs", []))
    print("[Loop] Already reviewed " + str(num_reviewed) + " PR(s)")

    try:
        while True:
            print("\n[Loop] Waiting for event... (loop is idle, no clock, no one watching)")
            print("[Loop] Heartbeat: event-driven - sits quiet until something arrives")

            # Wait for event (simulated - in reality, this is a GitHub webhook)
            event = simulate_github_event()
            event_type = event["action"]
            pr_number = event["pull_request"]["number"]
            pr_title = event["pull_request"]["title"]

            # Check if we already reviewed this PR
            reviewed_prs = spine.get("Reviewed PRs", [])
            if str(pr_number) in reviewed_prs:
                print("[Loop] [SKIP] Already reviewed PR #" + str(pr_number) + " - skipping")
                print("[Loop] Exit - going idle until next event")
                time.sleep(1)
                continue

            print("\n" + "=" * 50)
            print("[Event] pull_request opened event detected!")
            print("[Event] PR #" + str(pr_number) + ": " + pr_title)
            print("=" * 50 + "\n")

            # Loop fires fresh run
            print("[Loop] Loop fires fresh run - reacting to event")
            print("[Loop] Step 1: Checkout code, read diff, see what changed")

            changed_files = event["changed_files"]
            diff_summary = "Changed files: " + ", ".join(changed_files)
            print("[Loop] Changed files: " + ", ".join(changed_files))

            # Step 2: Runs reviewer agent
            print("[Loop] Step 2: Invoke reviewer agent with diff")
            review_result, review_reasons = simulate_reviewer(diff_summary)

            # Step 3: Take action based on review
            print("\n[Loop] Step 3: Take action based on reviewer result")

            if review_result == "PASS":
                print("[Loop] [PASS] - posting review on PR")
                print("[Loop] Review: 'Great work! No issues found.'")
                # Mark as reviewed in spine
                reviewed_prs.append(str(pr_number))
                spine["Reviewed PRs"] = reviewed_prs
                save_progress(spine)
                print("[Loop] Review posted. Loop exits - goes idle again.")
            else:
                print("[Loop] [FAIL] - posting review with reasons")
                print("[Loop] Review: 'Here are the issues found: " + review_reasons + "'")
                # Add pattern to spine
                patterns = spine.get("Patterns", [])
                patterns.append("PR #" + str(pr_number) + ": " + review_reasons)
                spine["Patterns"] = patterns
                save_progress(spine)
                print("[Loop] Review posted with specific reasons.")
                print("[Loop] Loop exits - goes idle until next event.")

            print("\n[Loop] Step 4: Loop exits - goes idle until next event")
            print("[Loop] No clock running - loop is quiet between events")
            print("[Loop] Wait for next pull_request event...")

            # Small delay before loop checks for next event
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")
        save_progress(spine)


if __name__ == "__main__":
    run_loop()