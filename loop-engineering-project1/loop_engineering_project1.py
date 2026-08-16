import time
import os
import pathlib

OUTPUT_FILE = pathlib.Path("output.txt")
POLL_INTERVAL = 2  # seconds


def simulate_long_running_task():
    """Simulate a task that takes some time to complete, then creates an output file."""
    print("[Task] Starting long-running operation...")
    time.sleep(5)  # Simulate 5 seconds of work
    OUTPUT_FILE.write_text("Task completed successfully!")
    print("[Task] Operation complete. Output file created.")


def check_completion():
    """Check if the output file exists (success condition)."""
    return OUTPUT_FILE.exists()


def run_loop():
    """In-session loop that polls periodically until the task completes."""
    print("[Loop] Starting in-session loop...")
    print(f"[Loop] Polling every {POLL_INTERVAL} seconds for output file...")
    print("[Loop] Press Ctrl-C to stop manually.\n")

    try:
        while True:
            if check_completion():
                print("\n[Loop] Success condition met: output file exists!")
                print("[Loop] Task is complete. Loop stopping.\n")
                break
            print(f"[Loop] ⏳ Still waiting... (checked at {time.strftime('%H:%M:%S')})")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")


if __name__ == "__main__":
    # Clean up any previous output file
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    # Start the simulated task in a non-blocking way
    # We'll run the task first, then the loop
    print("=" * 60)
    print("Loop Engineering: Project 1 - In-Session Loop")
    print("=" * 60)
    print()

    # Run the task first to create the output file
    simulate_long_running_task()

    # Then run the loop to check for completion
    run_loop()