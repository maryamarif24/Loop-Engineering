import time
import os
import pathlib
import json
import random

PROGRESS_FILE = pathlib.Path("progress.md")
INTERVAL_SECONDS = 3


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


def simulate_ci_triage(spine):
    """Simulate triaging overnight CI failures."""
    print("[Task] Starting morning CI triage...")
    candidates = []

    done_items = spine.get("Done", [])
    in_progress = spine.get("In progress", [])
    open_items = spine.get("Open / needs a human", [])

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


def simulate_draft_fix(task):
    """Simulate drafting a fix in isolated worktree."""
    print("[Task] Drafting fix for: " + task)
    print("[Task] Creating branch: claude/fix-" + task[:20].lower().replace(" ", "-"))
    print("[Task] Running reviewer agent on diff..." + "\n")
    return True


def simulate_reviewer(task):
    """Simulate separate reviewer agent grading the change."""
    print("[Reviewer] Grading fix for: " + task)
    result = random.choice(["PASS", "PASS", "FAIL"])
    if result == "PASS":
        print("[Reviewer] -> PASS: fix verified, low risk")
        return "PASS", "low"
    else:
        print("[Reviewer] -> FAIL: changes risky or failing")
        return "FAIL", "high"


def run_loop():
    """Scheduled loop with spine memory - simulates morning triage running unattended."""
    print("=" * 60)
    print("Loop Engineering: Project 3 - Scheduled Loop (Morning Brief with Memory)")
    print("=" * 60)
    print()

    spine = load_spine()
    print("[Loop] Loaded spine: " + str(len(spine.get("Done", []))) + " done, "
          + str(len(spine.get("In progress", []))) + " in progress, "
          + str(len(spine.get("Open / needs a human", []))) + " needing human decision")

    total_prs_opened = 0

    try:
        for run_num in range(1):
            print("\n[Loop] === Morning run #" + str(run_num + 1) + " ===")
            print("[Loop] Time: 9am weekday - heartbeat triggered")

            print("[Loop] Step 1: Read progress.md (spine memory)")

            candidates = simulate_ci_triage(spine)
            if not candidates:
                print("[Loop] No new candidates found - all caught up")
                break

            print("[Loop] Step 2: Processing candidates (max 5 per run)")

            for i, task in enumerate(candidates):
                if i >= 5:
                    print("[Loop] Reached max 5 PRs cap - stopping this run")
                    break

                print("[Loop] Candidate #" + str(i + 1) + ": " + task)

                if not simulate_draft_fix(task):
                    continue

                review_result, risk_level = simulate_reviewer(task)

                if review_result == "PASS" and risk_level == "low":
                    print("[Loop] PASS + low risk - opening PR")
                    total_prs_opened = total_prs_opened + 1
                    spine["Done"].append(task + " (PR opened, " + review_result + ")")
                else:
                    print("[Loop] FAIL or risky - writing to 'needs a human'")
                    spine["Open / needs a human"].append(task + " (" + review_result + ", risk: " + risk_level + ")")

                save_spine(spine)

            print("\n[Loop] === Run complete ===")
            print("[Loop] PRs opened this run: " + str(total_prs_opened))
            print("[Loop] Spine saved for tomorrow's run")
            print("[Loop] Loop exiting - tomorrow's run reads progress.md")

        print("\n[Overall] Total PRs opened: " + str(total_prs_opened))

    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")
        save_spine(spine)


if __name__ == "__main__":
    run_loop()