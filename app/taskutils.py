"""TaskFlow task utilities — COMPLETE LAB SOLUTION (Module 02).

This module is the *reference solution* for the Module 02 lab. It contains a
fully worked, heavily commented answer to every task in
`labs/module-02-lab.md`:

    Task 1      -> parse_task()           + InvalidTaskError
    Task 2      -> priority_score(), sort_tasks()
    Task 3      -> class Task
    Your Turn   -> high_priority_titles()
    Debug/Fix   -> add_tag()              (mutable-default bug fixed)
    Exercise A  -> ALLOWED_PRIORITIES set (single source of truth)
    Exercise B  -> length validation in parse_task()
    Stretch     -> Task.from_dict()

Exercise C (read config from the environment) lives in
`scripts/check_config.py` because it is a standalone script, not a task utility.

Everything here uses only the Python standard library, so it runs anywhere
with no installation. Run the live demo with:

    python demo.py
"""

# `from __future__ import annotations` makes Python treat every type hint
# (the `: dict`, `-> dict`, etc.) as a plain string instead of evaluating it
# at import time. This lets us write modern hints like `list[str] | None` even
# on older Python versions, and it slightly speeds up importing. It must be the
# first statement in the file.
from __future__ import annotations


# ---------------------------------------------------------------------------
# Exercise A — "Choose the right collection"
# ---------------------------------------------------------------------------
# These module-level constants are the SINGLE SOURCE OF TRUTH for the rules
# parse_task() enforces. Defining them once (here) means there is exactly one
# place to change if the rules change — every function below reads from these.

# We use a SET (curly braces, no key:value pairs) — NOT a list — for the
# allowed priorities. Why a set?
#   * Membership testing (`priority in ALLOWED_PRIORITIES`) is O(1) on a set,
#     versus O(n) on a list. With three items the speed difference is tiny,
#     but the *intent* is what matters: a set says "these are unique, unordered
#     values and all I care about is membership."
#   * A set automatically forbids duplicates, so the data structure itself
#     documents that each priority is a distinct, one-of-a-kind value.
ALLOWED_PRIORITIES = {"low", "medium", "high"}

# Exercise B uses this constant as the maximum allowed title length. Keeping it
# as a named constant (instead of a magic number `200` buried in the code)
# makes the rule self-documenting and easy to tune in one place.
MAX_TITLE_LENGTH = 200


# ---------------------------------------------------------------------------
# Task 1 (part 1) — a custom exception
# ---------------------------------------------------------------------------
class InvalidTaskError(ValueError):
    """Raised when a task record is missing or has an invalid field.

    We subclass `ValueError` (a built-in exception that means "right type,
    wrong value") rather than the generic `Exception`. That gives callers a
    choice: they can catch our *specific* `InvalidTaskError`, OR they can catch
    the broader `ValueError` and still handle it. A named, custom exception is
    self-documenting — a stack trace that says `InvalidTaskError` tells the
    reader exactly what went wrong, and in a later module it maps cleanly onto
    an HTTP 4xx response.

    The class body is just a docstring; it needs no extra code because it
    inherits everything it needs from `ValueError`. The `pass`-like docstring
    is enough to define a complete, usable exception type.
    """


# ---------------------------------------------------------------------------
# Task 1 (part 2) — parse and validate a raw task record
# Also includes Exercise B (length validation).
# ---------------------------------------------------------------------------
def parse_task(record: dict) -> dict:
    """Normalize a raw task record; raise InvalidTaskError on bad input.

    `parse_task` is the *boundary* of our system: messy, untrusted input goes
    in, and a clean, predictable dict comes out. Validating here — once — means
    every downstream function can trust the data and never re-check it.

    Args:
        record: a raw dict that may have stray whitespace, a missing title,
                or a free-text priority, e.g. {"title": " Ship ", "priority": "HIGH"}.

    Returns:
        A clean dict shaped exactly like:
            {"title": <non-empty str>, "priority": <one of ALLOWED_PRIORITIES>, "done": False}

    Raises:
        InvalidTaskError: if the title is missing/empty, or too long (Exercise B).
    """
    # `record.get("title", "")` reads the "title" key but returns the default
    # "" (empty string) if the key is ENTIRELY MISSING. This is the key trick:
    # `record["title"]` would raise a KeyError on `{}`, but `.get` lets us treat
    # "missing key" and "empty value" the same way. `.strip()` then removes
    # leading/trailing whitespace so " Ship " becomes "Ship".
    title = record.get("title", "").strip()

    # An empty string is "falsy" in Python, so `not title` is True for both a
    # missing title ("") and a whitespace-only title ("   " -> "" after strip).
    # This single check rejects every "no real title" case. We REJECT here
    # (rather than substitute a default) because a task with no title is
    # meaningless — there is nothing sensible to fall back to.
    if not title:
        raise InvalidTaskError("Task 'title' is required")

    # Exercise B — guard against absurdly long titles. We include the offending
    # length and the limit in the message so the error is actionable, e.g.
    # "Task 'title' too long (250 > 200)". An f-string (the f"..." syntax) lets
    # us embed `{len(title)}` and `{MAX_TITLE_LENGTH}` directly in the text.
    if len(title) > MAX_TITLE_LENGTH:
        raise InvalidTaskError(
            f"Task 'title' too long ({len(title)} > {MAX_TITLE_LENGTH})"
        )

    # Priority handling: default to "medium" if absent, strip whitespace, and
    # lowercase so "HIGH", "High", and "high" all normalize to "high".
    priority = record.get("priority", "medium").strip().lower()

    # DESIGN DECISION (be consistent!): unlike the title, we FORGIVE a bad
    # priority instead of rejecting it — an unrecognized priority quietly falls
    # back to "medium". Either policy (reject vs. forgive) is defensible; the
    # lesson is to pick one and apply it consistently. We forgive priority
    # because a slightly-wrong priority is recoverable, while a missing title
    # is not.
    if priority not in ALLOWED_PRIORITIES:
        priority = "medium"

    # Return the clean, canonical shape every other function can rely on.
    # `"done": False` is the sensible starting state for a brand-new task.
    return {"title": title, "priority": priority, "done": False}


# ---------------------------------------------------------------------------
# Task 2 — compute a priority score and sort
# ---------------------------------------------------------------------------
def priority_score(priority: str) -> int:
    """Return a numeric weight for sorting tasks by priority.

    Sorting needs numbers, not words. This maps the priority *labels* onto
    sortable *weights* so "high" outranks "medium" outranks "low".
    """
    # A local dict maps each label to its weight. Defined inside the function
    # because it is only used here.
    weights = {"low": 1, "medium": 2, "high": 3}

    # `weights.get(priority, 0)` returns the weight if the priority is known,
    # or the default `0` if it is not — so an unexpected value like "urgent"
    # yields 0 and NEVER raises KeyError. This "safe lookup with a default" is
    # the defensive choice: the function degrades gracefully instead of
    # crashing the whole sort.
    return weights.get(priority, 0)


def sort_tasks(tasks: list[dict]) -> list[dict]:
    """Return tasks ordered by priority, highest first.

    Args:
        tasks: a list of task dicts (each must have a "priority" key).

    Returns:
        A NEW list, sorted high -> low. The input list is left untouched.
    """
    # `sorted(...)` returns a brand-new sorted list (it does NOT mutate the
    # original, unlike list.sort()). That makes this function "pure" and
    # predictable — callers never get surprised by their input changing.
    #
    # `key=...` tells sorted HOW to compare items: for each task `t`, compute a
    # sort key. We use a `lambda` (a tiny, unnamed, one-line function) that maps
    # each task to its numeric priority score.
    #
    # `reverse=True` flips the order so the HIGHEST score comes first.
    #
    # Python's sort is "stable": tasks with equal priority keep their original
    # relative order, which gives predictable, repeatable output.
    return sorted(tasks, key=lambda t: priority_score(t["priority"]), reverse=True)


# ---------------------------------------------------------------------------
# Your Turn — filter helper: titles of high-priority tasks
# ---------------------------------------------------------------------------
def high_priority_titles(tasks: list[dict]) -> list[str]:
    """Return the titles of high-priority tasks, in their original order.

    Args:
        tasks: a list of task dicts.

    Returns:
        A list of title strings for tasks whose priority is exactly "high".
    """
    # This is a LIST COMPREHENSION — a compact, idiomatic way to build a new
    # list by filtering an existing one. Read it left-to-right as a sentence:
    #   "Give me t['title']  ... for each task t in tasks  ... but only IF
    #    that task's priority is 'high'."
    # It builds a NEW list (no mutation of `tasks`) and preserves original
    # order because it walks `tasks` front-to-back. We reach for a comprehension
    # here because the logic is a simple map+filter that fits readably on one
    # line; a multi-line `for` loop would be more code for the same result.
    return [t["title"] for t in tasks if t["priority"] == "high"]


# ---------------------------------------------------------------------------
# Debug / Fix — the mutable-default-argument trap
# ---------------------------------------------------------------------------
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Append a tag to a list, creating a fresh list when none is given.

    THE BUG WE FIXED (from the starter file):
        def add_tag(tag, tags=[]):   # <-- BROKEN
            tags.append(tag)
            return tags

    A function's default argument value is created EXACTLY ONCE, when Python
    first *defines* the function — NOT each time the function is *called*. So
    `tags=[]` builds a single list that is shared by every call that does not
    pass its own list. Each call appends to that same shared list, so it grows:
    three separate `add_tag("urgent")` calls would return ['urgent'], then
    ['urgent', 'urgent'], then ['urgent', 'urgent', 'urgent'].

    THE FIX — the "None sentinel" pattern:
        * Default to `None`, which is immutable and therefore safe to share.
        * Inside the function, detect "no list was passed" and build a brand-new
          list on each such call.
    """
    # `is None` checks object IDENTITY (is this the actual None object?), which
    # is the correct, idiomatic way to test for None — never `== None`. When the
    # caller did not supply a list, we create a FRESH one here, so every default
    # call starts from an empty list and nothing leaks between calls.
    if tags is None:
        tags = []

    # Now it is safe to mutate `tags`: it is either the caller's own list or a
    # fresh one we just made.
    tags.append(tag)
    return tags


# ---------------------------------------------------------------------------
# Task 3 — the Task class (and the Stretch Goal classmethod)
# ---------------------------------------------------------------------------
class Task:
    """A single TaskFlow task: data bundled together with a little behavior.

    A class is a blueprint for creating objects. Each `Task` object carries its
    own data (title, priority, done) AND the behavior that acts on that data
    (complete, repr). Bundling the two together is the core idea of
    object-oriented programming.
    """

    def __init__(self, title: str, priority: str = "medium"):
        """Initialize a new Task.

        `__init__` is the CONSTRUCTOR — Python runs it automatically when you
        write `Task("Ship release", "high")`. `self` is the brand-new object
        being built; assigning to `self.<name>` stores data ON that object as
        an "attribute". `priority="medium"` is a DEFAULT, so callers may omit it.
        """
        self.title = title         # store the title on this object
        self.priority = priority   # store the priority (defaults to "medium")
        self.done = False          # every new task starts as not-done

    def complete(self) -> None:
        """Mark this task as done.

        This is a METHOD — a function attached to the object. It represents the
        "behavior" half of "data plus behavior": it changes this task's state.
        `-> None` documents that it returns nothing; it mutates `self` instead.
        """
        self.done = True

    def __repr__(self) -> str:
        """Return the unambiguous, debug-friendly string form of this Task.

        `__repr__` controls what you see when you `print(task)` or inspect a
        Task in the REPL or in a failing test. Without it you'd get an opaque
        `<Task object at 0x10f3a2b50>`, which tells you nothing. With it you get
        `Task(title='Ship release', priority='high', done=True)` — exactly what
        you need to debug. The `!r` in the f-string calls `repr()` on each value
        so strings appear WITH their quotes ('high' not high), removing any
        ambiguity about types.
        """
        return (
            f"Task(title={self.title!r}, priority={self.priority!r}, "
            f"done={self.done})"
        )

    @classmethod
    def from_dict(cls, record: dict) -> "Task":
        """Stretch Goal — build a validated Task from a raw record.

        `@classmethod` makes this an "alternative constructor": instead of
        receiving an instance (`self`), it receives the CLASS itself (`cls`).
        That lets us offer a second, convenient way to create a Task — straight
        from a messy raw dict — while reusing all of parse_task()'s validation.

        This is the clean entry point that connects validation (parse_task) and
        the class: untrusted dict in, fully-validated Task out.
        """
        # Run the raw record through the SAME validation every other input uses.
        # If the record is invalid, parse_task raises InvalidTaskError here.
        data = parse_task(record)

        # `cls(...)` is equivalent to `Task(...)`, but using `cls` keeps the
        # method correct even if the class is later renamed or subclassed.
        return cls(title=data["title"], priority=data["priority"])
