import time
import os
import pathlib
from datetime import datetime

PROGRESS_FILE = pathlib.Path("progress.md")
POLL_INTERVAL = 1  # seconds (short for demo; would be minutes/hours in production)
MAX_INNER_TRIES = 3  # max retries for inner loop failures


def get_last_batch_progress():
    """Get the last batch progress from the progress/spine file."""
    if PROGRESS_FILE.exists():
        content = PROGRESS_FILE.read_text().strip()
        if content:
            try:
                return content
            except ValueError:
                pass
    return None


def update_batch_progress(items_processed, items_failed, status="in_progress"):
    """Update the progress/spine file with batch progress."""
    timestamp = datetime.now().isoformat()
    progress = f"""# Nested Loop Batch Progress

**Last updated**: {timestamp}

**Batch Status**: {status}
**Items Processed**: {items_processed}
**Items Failed**: {items_failed}

## Item Details

"""
    # Read existing details and append
    if PROGRESS_FILE.exists():
        existing = PROGRESS_FILE.read_text()
        # Keep existing details but add new summary
        progress += existing

    PROGRESS_FILE.write_text(progress)


def run_inner_loop(item_id):
    """Run an inner conditional loop for a single item."""
    print(f"[Inner Loop] Starting inner loop for item {item_id}...")
    print(f"[Inner Loop] Running conditional check loop (max {MAX_INNER_TRIES} tries)...")

    for try_num in range(1, MAX_INNER_TRIES + 1):
        print(f"[Inner Loop] Try {try_num}/{MAX_INNER_TRIES} for item {item_id}...")

        # Simulate a conditional check - sometimes succeeds, sometimes fails
        success = try_num == MAX_INNER_TRIES or (try_num > 1 and item_id % 2 == 0)

        if success:
            print(f"[Inner Loop] Item {item_id} PASS after try {try_num}")
            return True

        print(f"[Inner Loop] Item {item_id} FAIL on try {try_num}")

        if try_num < MAX_INNER_TRIES:
            print(f"[Inner Loop] Retrying item {item_id}...")
            time.sleep(POLL_INTERVAL)
        else:
            print(f"[Inner Loop] Item {item_id} exhausted all tries.")

    return False


def run_outer_loop(batch_size):
    """Outer supervisory loop that manages inner loops with error recovery."""
    print("=" * 60)
    print("Loop Engineering: Project 7 - Nested Loop with Error Recovery")
    print("=" * 60)
    print()

    print(f"[Outer Loop] Starting batch processing of {batch_size} items...")
    print(f"[Outer Loop] Each item has an inner conditional loop with {MAX_INNER_TRIES} max tries")
    print(f"[Outer Loop] Error recovery: retry, then escalate if needed")
    print()

    items_processed = 0
    items_failed = 0

    for item_id in range(1, batch_size + 1):
        print(f"\n[Outer Loop] Processing item {item_id} of {batch_size}...")

        # Check previous progress for this item
        last_progress = get_last_batch_progress()
        if last_progress and f"item {item_id}" in last_progress:
            print(f"[Outer Loop] Item {item_id} was previously processed - checking status...")

        # Run the inner loop
        inner_success = run_inner_loop(item_id)

        if inner_success:
            items_processed += 1
            print(f"[Outer Loop] Item {item_id} - overall success")
        else:
            items_failed += 1
            print(f"[Outer Loop] ❌ Item {item_id} - failing, escalating...")

            # Error recovery: try once more with different approach
            print(f"[Outer Loop] Running error recovery for item {item_id}...")
            time.sleep(POLL_INTERVAL)
            recovery_success = run_inner_loop(item_id)  # Retry

            if recovery_success:
                items_processed += 1
                print(f"[Outer Loop] Item {item_id} recovered on retry")
            else:
                print(f"[Outer Loop] Item {item_id} escalated for human decision")

        # Update spine after each item
        update_batch_progress(items_processed, items_failed, "completed")

    # Final summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Items Processed: {items_processed}/{batch_size}")
    print(f"Items Failed: {items_failed}/{batch_size}")
    print(f"Success Rate: {(items_processed/batch_size)*100:.1f}%")
    print()
    print("Progress remembered in progress.md (spine) for next run.")


if __name__ == "__main__":
    # Clean up previous progress file
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()

    # Run the nested loop
    batch_size = 5  # Process 5 items per run
    run_outer_loop(batch_size)