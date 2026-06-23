# Module 02 Lab — Complete Reference Solution

A fully worked, heavily commented reference solution to **every** exercise in the
Module 02 lab (*Build the `taskutils` Module*) for the TaskFlow backend course.

Use this repo to check your own work **after** you have attempted the lab. Every
line of code is commented to explain not just *what* it does but *why* it is
written that way.

> ⚠️ **Learning tip:** Try each task yourself first. Reading the solution is most
> useful as a way to compare approaches and understand the reasoning — not as a
> shortcut past the practice that builds the skill.

---

## How to run it

No installation is needed for the core solution — it uses only the Python
standard library.

```bash
# From the repository root:
python demo.py                 # runs and prints every task's solution
python scripts/check_config.py # Exercise C (config from the environment)
```

Optional (only enhances Exercise C, lets it read a local `.env` file):

```bash
python -m pip install -r requirements.txt
```

---

## Repository layout

```
module-02-lab-solution/
├── README.md                 # you are here
├── requirements.txt          # optional dep (python-dotenv) for Exercise C only
├── .gitignore
├── demo.py                   # runnable demo that exercises every solution
├── app/
│   ├── __init__.py           # marks `app` as an importable package
│   └── taskutils.py          # ★ the main solution: Tasks 1–3, Your Turn,
│                             #   Debug/Fix, Exercises A & B, Stretch Goal
└── scripts/
    └── check_config.py       # Exercise C — read config from the environment
```

The heart of the solution is [`app/taskutils.py`](app/taskutils.py). It mirrors
the `app/taskutils.py` file you build during the lab. The only piece that lives
elsewhere is Exercise C, which is a standalone startup script rather than a task
utility, so it sits in [`scripts/check_config.py`](scripts/check_config.py).

---

## Where each exercise is solved

| Lab item | Solution location | Symbol / section |
| --- | --- | --- |
| **Task 1** — Parse & validate a record | `app/taskutils.py` | `InvalidTaskError`, `parse_task()` |
| **Task 2** — Priority score & sorting | `app/taskutils.py` | `priority_score()`, `sort_tasks()` |
| **Task 3** — The `Task` class | `app/taskutils.py` | `class Task` (`__init__`, `complete`, `__repr__`) |
| **🧠 Your Turn** — Filter helper | `app/taskutils.py` | `high_priority_titles()` |
| **🧩 Debug/Fix** — Mutable-default trap | `app/taskutils.py` | `add_tag()` (fixed with the `None` sentinel) |
| **Exercise A** — Choose the right collection | `app/taskutils.py` | `ALLOWED_PRIORITIES` set (used in `parse_task`) |
| **Exercise B** — Validate with a custom exception | `app/taskutils.py` | length check in `parse_task()` + `MAX_TITLE_LENGTH` |
| **Exercise C** — Read config from the environment | `scripts/check_config.py` | `report_database_url()` |
| **Stretch Goal** — `Task.from_dict` | `app/taskutils.py` | `Task.from_dict()` classmethod |

---

## Solution notes by exercise

### Task 1 — `parse_task` + `InvalidTaskError`
The boundary where messy input becomes clean, trusted data. Validates once so
every downstream function can rely on the shape `{"title", "priority", "done"}`.
A missing/empty title is **rejected**; an unknown priority is **forgiven**
(falls back to `"medium"`) — a deliberate, consistent design choice.

### Task 2 — `priority_score` + `sort_tasks`
Maps priority labels to sortable numbers, then uses `sorted(..., key=..., reverse=True)`
to return a **new** high→low list without mutating the input. `priority_score`
uses a safe `.get(..., 0)` lookup so unknown values never crash the sort.

### Task 3 — `class Task`
Bundles data (`title`, `priority`, `done`) with behavior (`complete`) and a
debug-friendly `__repr__`. A good `__repr__` turns an opaque
`<Task object at 0x…>` into `Task(title='…', priority='…', done=…)`.

### 🧠 Your Turn — `high_priority_titles`
A single-line **list comprehension** that filters to high-priority titles while
preserving order and leaving the input untouched.

### 🧩 Debug/Fix — `add_tag`
Fixes the classic mutable-default-argument bug. The default `[]` is created once
at definition time and shared across calls; the fix defaults to `None` and
creates a fresh list inside the function on each call.

### Exercise A — the `ALLOWED_PRIORITIES` set
A **set** is the right collection: O(1) membership and uniqueness, declared once
at module level as the single source of truth.

### Exercise B — length validation
Rejects titles longer than `MAX_TITLE_LENGTH` with a descriptive
`InvalidTaskError` that includes the offending length.

### Exercise C — `report_database_url`
Reads `DATABASE_URL` from the environment and reports **only** whether it is set
— never the secret value itself.

### Stretch Goal — `Task.from_dict`
An alternative constructor (`@classmethod`) that runs a raw record through
`parse_task` and returns a fully validated `Task` — connecting validation and
the class in one clean entry point.

---

## Validation checklist

This solution satisfies every item in the lab's success criteria:

- [x] `parse_task` normalizes valid records and raises `InvalidTaskError` on bad input.
- [x] `priority_score` returns `0` for unknown; `sort_tasks` orders high → low.
- [x] `high_priority_titles` works via a comprehension.
- [x] `add_tag` is fixed with the `None` sentinel — three calls each return `['urgent']`.
- [x] `Task` has `__init__`, `complete()`, and a readable `__repr__`.
- [x] `app/taskutils.py` imports cleanly from the project root.
