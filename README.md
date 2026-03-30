# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## Smarter Scheduling

Beyond the basic daily plan, `pawpal_system.py` includes three algorithmic improvements:

- **Sort by time** — `Scheduler.sort_by_time()` orders tasks by `start_time` (HH:MM), with untimed tasks placed last.
- **Filter tasks** — `Scheduler.filter_tasks()` returns tasks matching a completion status, a pet name, or both.
- **Recurring tasks** — `Task` supports `frequency` (`"once"`, `"daily"`, `"weekly"`). Calling `mark_complete()` on a recurring task automatically advances its `due_date` using `timedelta` instead of removing it.
- **Conflict detection** — `Scheduler.detect_conflicts()` warns when two tasks share the same `start_time`, preventing accidental double-booking.

## Testing PawPal+

Run the full test suite with:

```bash
.venv/bin/python -m pytest tests/test_pawpal.py -v
```

The suite covers 12 tests across four areas:

| Area | What is tested |
|---|---|
| **Task completion** | `mark_complete()` sets `is_completed`; `once` tasks stay done |
| **Sorting** | Tasks returned in chronological HH:MM order; untimed tasks go last |
| **Recurrence** | Daily tasks reschedule to tomorrow; weekly to next week; `is_completed` resets |
| **Conflict detection** | Duplicate `start_time` triggers a warning; unique times and no-time tasks are safe |
| **Edge cases** | Empty pet task list returns an empty plan; tasks exceeding the time budget are skipped |

**Confidence level: ★★★★☆** — Core scheduling behaviors are well covered. Not yet tested: multi-pet conflict detection across pets, preference-based ordering, or UI integration.

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
