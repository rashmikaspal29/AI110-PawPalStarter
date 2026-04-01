# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner intelligently plan and manage daily care tasks for their pets.

## Features

- **Add owner & pet** — store owner and pet info that persists across the session
- **Add tasks** — assign tasks with title, time, duration, priority, and frequency
- **Priority scheduling** — generates a daily schedule sorted by high → medium → low priority
- **Sorting by time** — view your schedule in chronological `HH:MM` order
- **Conflict warnings** — detects and displays tasks scheduled at the exact same time
- **Daily recurrence** — marking a daily or weekly task complete auto-creates the next occurrence
- **Filter by status** — view all, pending, or completed tasks instantly

## Demo

Run the app locally:

```bash
python -m streamlit run app.py
```

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

Tests cover:
- **Sorting correctness** — tasks are returned in chronological order by `HH:MM`
- **Recurrence logic** — marking a `daily` or `weekly` task complete creates a new instance for the next occurrence
- **Conflict detection** — `Scheduler` flags tasks scheduled at the exact same time
- **Filtering** — tasks can be filtered by pet name or completion status
- **Edge cases** — no tasks, single task, non-recurring tasks, no conflicts

Confidence level: ⭐⭐⭐⭐⭐ (5/5) — all 12 tests pass covering happy paths and edge cases.

## Smarter Scheduling

The scheduler now includes algorithmic intelligence beyond basic priority sorting:

- **Sort by time** — `Scheduler.sort_by_time()` orders tasks by their `HH:MM` scheduled time using a lambda key.
- **Filter tasks** — `Scheduler.filter_tasks(pet_name, completed)` returns tasks matching a specific pet or completion status.
- **Recurring tasks** — `Task.mark_complete()` automatically creates the next occurrence for `daily` or `weekly` tasks using Python's `timedelta`.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans for tasks scheduled at the exact same time and returns warning messages instead of crashing.
