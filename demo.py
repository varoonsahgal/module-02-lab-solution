"""Runnable demonstration of every Module 02 lab solution.

This script exercises each function and class from `app/taskutils.py` and
prints the results, so you can run ONE command and watch every task's solution
work end to end:

    python demo.py

Each section below is labeled with the lab task it demonstrates.
"""

from app.taskutils import (
    InvalidTaskError,
    Task,
    add_tag,
    high_priority_titles,
    parse_task,
    priority_score,
    sort_tasks,
)


def main() -> None:
    """Run every demonstration in order, printing labeled output."""

    # --- Task 1: parse_task normalizes good input and rejects bad input ------
    print("== Task 1: parse_task ==")
    clean = parse_task({"title": " Ship release ", "priority": "HIGH"})
    print("valid record ->", clean)
    try:
        # An empty title must be rejected with our custom exception.
        parse_task({"title": "", "priority": "low"})
    except InvalidTaskError as exc:
        print("invalid record -> InvalidTaskError:", exc)

    # --- Task 2: scoring and sorting -----------------------------------------
    print("\n== Task 2: priority_score + sort_tasks ==")
    tasks = [
        parse_task({"title": "Cleanup", "priority": "low"}),
        parse_task({"title": "Hotfix", "priority": "high"}),
        parse_task({"title": "Docs", "priority": "medium"}),
    ]
    print("scores ->", [priority_score(t["priority"]) for t in tasks])
    print("sorted high->low ->", [t["title"] for t in sort_tasks(tasks)])

    # --- Your Turn: high_priority_titles -------------------------------------
    print("\n== Your Turn: high_priority_titles ==")
    print("high-priority titles ->", high_priority_titles(tasks))

    # --- Debug/Fix: add_tag no longer accumulates across calls ---------------
    print("\n== Debug/Fix: add_tag (mutable-default bug fixed) ==")
    print("call 1 ->", add_tag("urgent"))
    print("call 2 ->", add_tag("urgent"))
    print("call 3 ->", add_tag("urgent"))

    # --- Task 3 + Stretch: the Task class and from_dict ----------------------
    print("\n== Task 3: Task class ==")
    task = Task("Ship release", "high")
    print("before complete ->", task)
    task.complete()
    print("after complete  ->", task)

    print("\n== Stretch: Task.from_dict ==")
    built = Task.from_dict({"title": "  Deploy ", "priority": "HIGH"})
    print("from_dict -> ", built)


if __name__ == "__main__":
    main()
