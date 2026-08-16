import time
import os
import pathlib
from datetime import datetime, timedelta

PROGRESS_FILE = pathlib.Path("progress.md")
OUTPUT_FILE = pathlib.Path("daily_summary.txt")
POLL_INTERVAL = 60  # seconds (1 minute for demo; would be hours in production)


def get_last_run_time():
    """Get the last run time from the progress/spine file."""
    if PROGRESS_FILE.exists():
        content = PROGRESS_FILE.read_text().strip()
        if content:
            try:
                return datetime.fromisoformat(content)
            except ValueError:
                pass
    return None


def update_last_run_time():
    """Update the progress/spine file with the current run time."""
    PROGRESS_FILE.write_text(datetime.now().isoformat())


def check_for_new_items():
    """Check if there are new items since last run."""
    # Simulate checking for new items - in a real scenario this would check
    # a ticket system, CI results, inbox, etc.
    print("[Check] Looking for new items since last run...")

    last_run = get_last_run_time()
    now = datetime.now()

    if last_run is None:
        print("[Check] No previous run found - this is the first run.")
        return True  # Treat as "new items found"

    time_since_last = now - last_run
    hours_since_last = time_since_last.total_seconds() / 3600

    if hours_since_last < 1:
        print(f"[Check] Last run was {hours_since_last:.1f} hour(s) ago - no new items yet.")
        return False

    print(f"[Check] {hours_since_last:.1f} hours since last run - processing new items.")
    return True


def process_items():
    """Process new items and generate summary."""
    print("[Processing] Processing new items...")

    now = datetime.now()

    # Simulate processing items
    time.sleep(2)

    summary = f"""# Daily Summary - {now.strftime('%Y-%m-%d')}

## Items Processed: 3

1. Item A: Completed review
2. Item B: Fixed CI failure
3. Item C: Updated documentation

## Total: 3 items processed successfully

*Generated automatically by daily summary loop*
"""

    OUTPUT_FILE.write_text(summary)
    print("[Processing] Summary generated.")


def run_loop():
    """Periodic daily summary loop."""
    print("[Loop] Starting daily summary loop...")
    print(f"[Loop] Running every {POLL_INTERVAL} seconds (simulated daily schedule)")
    print("[Loop] Progress is remembered between runs via progress.md (spine)")
    print("[Loop] Press Ctrl-C to stop manually.\n")

    try:
        while True:
            if check_for_new_items():
                process_items()
                update_last_run_time()
                print("\n[Loop] Daily summary complete. Loop stopping until next scheduled run.\n")
            else:
                print(f"[Loop] ⏳ No new items yet. (checked at {time.strftime('%H:%M:%S')})")
                print("[Loop] Will check again at next beat.\n")

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")


if __name__ == "__main__":
    # Clean up any previous output/progress files
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()

    print("=" * 60)
    print("Loop Engineering: Project 6 - Daily Summary Loop")
    print("=" * 60)
    print()

    # Run the loop
    run_loop()