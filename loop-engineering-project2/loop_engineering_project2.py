import time
import os
import pathlib

SIMULATE_TESTS_PASS_AFTER = 3  # number of retry attempts until "tests pass"
MAX_TRIES = 8
POLL_INTERVAL = 1


def simulate_test_suite():
    """Simulate a test suite that passes after a number of retries."""
    print("[Task] Starting test suite simulation...")
    print(f"[Task] Tests will pass after {SIMULATE_TESTS_PASS_AFTER} attempt(s).")
    print(f"[Task] Max tries cap: {MAX_TRIES}\n")


def run_tests(tries):
    """Simulate running tests. Returns True if tests pass, False otherwise."""
    print(f"[Task] Running tests (attempt {tries} of {MAX_TRIES})...")
    if tries >= SIMULATE_TESTS_PASS_AFTER:
        print("[Task] [PASS] Tests PASSED")
        return True
    print("[Task] [FAIL] Tests FAILED - retrying...")
    return False


def check_no_progress(prev_args, current_args):
    """Check if the agent is repeating the same action with same arguments."""
    if prev_args == current_args:
        print("[Safety] [WARN] No progress detected - repeating same action")
        return True
    return False


def run_loop():
    """Conditional loop that runs until tests pass, with safety caps."""
    print("[Loop] Starting conditional loop (run-until-done)...")
    print(f"[Loop] Goal: Run tests until they PASS")
    print(f"[Loop] Safety: Max {MAX_TRIES} tries, no-progress check active\n")

    tries = 0
    prev_args = None

    try:
        while tries < MAX_TRIES:
            tries += 1
            print(f"[Loop] Try #{tries}/{MAX_TRIES}")

            # No-progress check
            if check_no_progress(prev_args, "run_tests"):
                print("[Loop] [STOP] Stopping: no progress detected")
                print("[Loop] Loop stopped - no progress after repeated attempts\n")
                return

            # Run tests
            test_passed = run_tests(tries)

            if test_passed:
                print("\n[Loop] [PASS] Success condition met: tests PASS!")
                print("[Loop] Task is complete. Loop stopping.\n")
                break

            # Wait before retry
            prev_args = "run_tests"
            time.sleep(POLL_INTERVAL)

        if tries >= MAX_TRIES:
            print("\n[Loop] [STOP] Max tries reached - loop stopping")
            print("[Loop] Safety limit hit. Task not complete within allowed attempts.\n")

    except KeyboardInterrupt:
        print("\n[Loop] Manual stop (Ctrl-C) detected. Loop exiting.")


if __name__ == "__main__":
    print("=" * 60)
    print("Loop Engineering: Project 2 - Conditional Loop (Run-Until-Done)")
    print("=" * 60)
    print()

    simulate_test_suite()
    run_loop()