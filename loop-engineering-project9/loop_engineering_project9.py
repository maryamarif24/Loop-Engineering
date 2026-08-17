import time
import os
import pathlib
from datetime import datetime
from collections import defaultdict

PROGRESS_FILE = pathlib.Path("progress.md")
POLL_INTERVAL = 1  # seconds (short for demo; would be minutes/hours in production)
MAX_ITEMS_PER_RUN = 3  # cap how many items processed per run


# Priority levels (higher number = higher priority)
PRIORITY_HIGH = 3
PRIORITY_MEDIUM = 2
PRIORITY_LOW = 1


def load_queue_state():
    """Load the priority queue state from the progress/spine file."""
    if PROGRESS_FILE.exists():
        content = PROGRESS_FILE.read_text().strip()
        if content:
            queue = {"high": [], "medium": [], "low": [], "completed": []}
            section_map = {
                "High Priority": "high",
                "Medium Priority": "medium",
                "Low Priority": "low",
                "Completed": "completed"
            }
            current_section = None
            for line in content.split('\n'):
                line_stripped = line.strip()
                mapped_section = None
                for label, key in section_map.items():
                    if line_stripped.startswith("## " + label):
                        mapped_section = key
                        break
                if mapped_section:
                    current_section = mapped_section
                elif line_stripped and current_section and line_stripped.startswith("- "):
                    item = line_stripped[2:].strip()
                    if current_section in queue:
                        queue[current_section].append(item)
            return queue
    return {"high": [], "medium": [], "low": [], "completed": []}


def save_queue_state(queue):
    """Save the priority queue state to the progress/spine file."""
    lines = []
    lines.append("## High Priority")
    for item in queue.get("high", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## Medium Priority")
    for item in queue.get("medium", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## Low Priority")
    for item in queue.get("low", []):
        lines.append("- " + item)
    lines.append("")
    lines.append("## Completed")
    for item in queue.get("completed", []):
        lines.append("- " + item)
    lines.append("")
    PROGRESS_FILE.write_text("\n".join(lines))


def get_priority(item):
    """Determine priority of an item - in a real scenario this might check item attributes."""
    # Simple heuristic: items starting with certain letters get high priority
    if item.startswith(("A", "B", "Urgent", "Fix", "Critical")):
        return PRIORITY_HIGH
    elif item.startswith(("C", "D", "Important", "D")):
        return PRIORITY_MEDIUM
    else:
        return PRIORITY_LOW


def process_item(item_id):
    """Process a single item."""
    print(f"[Queue] Processing item {item_id} (priority {get_priority(item_id)})...")
    time.sleep(1)  # Simulate work
    print(f"[Queue] Item {item_id} processed successfully")
    return True


def topological_sort_items(items, dependencies):
    """Simple sort by priority - items with higher priority processed first."""
    # Sort by priority level, then alphabetically within same priority
    return sorted(items, key=lambda x: (get_priority(x), x))


def run_loop():
    """Priority-queue loop that processes items by priority level."""
    print("=" * 60)
    print("Loop Engineering: Project 9 - Priority Queue Loop")
    print("=" * 60)
    print()

    # Define the item queue for this run - items with various priorities
    all_items = [
        "Fix auth token refresh bug",
        "Update lodash dependency",
        "Refactor data service",
        "Critical security patch",
        "Update README documentation",
        "Performance optimization",
        "Critical bug fix for payment",
        "Code style cleanup",
    ]

    # Load previous progress (spine memory)
    previous_queue = load_queue_state()
    already_completed = set(previous_queue.get("completed", []))

    # Filter to only items not yet completed
    remaining = [item for item in all_items if item not in already_completed]

    print(f"[Queue] Spine memory: {len(already_completed)} items previously completed")
    print(f"[Queue] Item pool: {', '.join(all_items)}")
    print(f"[Queue] Remaining items: {', '.join(remaining) if remaining else 'None - all done!'}")
    print(f"[Queue] Priority levels: High (security/bug fixes), Medium (docs/optimization), Low (cleanup)")
    print()

    # Sort remaining items by priority
    sorted_items = topological_sort_items(remaining, {})

    # Categorize by priority
    queue = {"high": [], "medium": [], "low": []}
    for item in sorted_items:
        priority = get_priority(item)
        if priority == PRIORITY_HIGH:
            queue["high"].append(item)
        elif priority == PRIORITY_MEDIUM:
            queue["medium"].append(item)
        else:
            queue["low"].append(item)

    # Process items in priority order, capped per run
    newly_processed = []

    # Process high priority first
    for item in queue["high"][:MAX_ITEMS_PER_RUN]:
        if process_item(item):
            newly_processed.append(item)
        time.sleep(POLL_INTERVAL)

    remaining_high = len(queue["high"]) - len([item for item in newly_processed if item in queue["high"]])
    # Process medium priority next (if capacity remains)
    medium_cap = MAX_ITEMS_PER_RUN - len([item for item in newly_processed if item in queue["high"]])
    for item in queue["medium"][:medium_cap]:
        if process_item(item):
            newly_processed.append(item)
        time.sleep(POLL_INTERVAL)

    # Process low priority last (if capacity remains)
    low_cap = MAX_ITEMS_PER_RUN - len(newly_processed)
    for item in queue["low"][:low_cap]:
        if process_item(item):
            newly_processed.append(item)
        time.sleep(POLL_INTERVAL)

    # Update spine with all completed items
    all_completed = already_completed | set(newly_processed)

    # Re-categorize remaining for spine
    remaining_items = [item for item in all_items if item not in all_completed]
    new_queue = {"high": [], "medium": [], "low": [], "completed": list(all_completed)}

    # Re-assign remaining items to priority queues
    for item in remaining_items:
        if get_priority(item) == PRIORITY_HIGH:
            new_queue["high"].append(item)
        elif get_priority(item) == PRIORITY_MEDIUM:
            new_queue["medium"].append(item)
        else:
            new_queue["low"].append(item)

    save_queue_state(new_queue)

    # Report
    remaining = [item for item in all_items if item not in all_completed]
    print()
    print(f"[Queue] Summary: {len(newly_processed)} items processed this run")
    print(f"[Queue] Total completed: {len(all_completed)}/{len(all_items)}")
    print(f"[Queue] Remaining in queue: {', '.join(remaining) if remaining else 'None - all caught up!'}")
    print()
    print("Progress remembered in progress.md (spine) for next run.")


if __name__ == "__main__":
    # Run the priority queue loop
    run_loop()