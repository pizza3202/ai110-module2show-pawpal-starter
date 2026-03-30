import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Original tests ─────────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", category="walk", duration=20, priority="high")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(name="Breakfast", category="feed", duration=10, priority="high"))
    pet.add_task(Task(name="Evening Walk", category="walk", duration=15, priority="medium"))
    assert len(pet.tasks) == 2


# ── Sorting correctness ────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Alex", available_time_per_day=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Dinner",        category="feed", duration=10, priority="high", start_time="18:00"))
    pet.add_task(Task(name="Morning Walk",  category="walk", duration=20, priority="high", start_time="07:00"))
    pet.add_task(Task(name="Flea Medicine", category="medication", duration=5, priority="medium", start_time="09:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    times = [t.start_time for t in sorted_tasks]
    assert times == ["07:00", "09:00", "18:00"]


def test_sort_by_time_puts_untimed_tasks_last():
    owner = Owner(name="Alex", available_time_per_day=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Brush Fur",    category="grooming", duration=15, priority="low"))  # no time
    pet.add_task(Task(name="Morning Walk", category="walk",     duration=20, priority="high", start_time="07:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    assert sorted_tasks[-1].start_time is None


# ── Recurrence logic ───────────────────────────────────────────────────────────

def test_daily_task_reschedules_to_tomorrow():
    task = Task(name="Morning Walk", category="walk", duration=20, priority="high", frequency="daily")
    task.mark_complete()
    expected = str(date.today() + timedelta(days=1))
    assert task.due_date == expected
    assert task.is_completed is False  # still active for tomorrow


def test_weekly_task_reschedules_to_next_week():
    task = Task(name="Bath", category="grooming", duration=30, priority="medium", frequency="weekly")
    task.mark_complete()
    expected = str(date.today() + timedelta(weeks=1))
    assert task.due_date == expected
    assert task.is_completed is False


def test_once_task_stays_completed():
    task = Task(name="Vet Visit", category="medication", duration=60, priority="high", frequency="once")
    task.mark_complete()
    assert task.is_completed is True


# ── Conflict detection ─────────────────────────────────────────────────────────

def test_no_conflicts_when_times_are_unique():
    owner = Owner(name="Alex", available_time_per_day=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Walk",      category="walk", duration=20, priority="high", start_time="07:00"))
    pet.add_task(Task(name="Breakfast", category="feed", duration=10, priority="high", start_time="08:00"))
    owner.add_pet(pet)
    assert Scheduler(owner=owner).detect_conflicts() == []


def test_conflict_detected_for_duplicate_start_times():
    owner = Owner(name="Alex", available_time_per_day=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Walk",     category="walk",        duration=20, priority="high",   start_time="08:00"))
    pet.add_task(Task(name="Feeding",  category="feed",        duration=10, priority="high",   start_time="08:00"))
    owner.add_pet(pet)
    conflicts = Scheduler(owner=owner).detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_for_tasks_without_start_time():
    owner = Owner(name="Alex", available_time_per_day=60)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Walk",     category="walk",    duration=20, priority="high"))
    pet.add_task(Task(name="Grooming", category="grooming", duration=15, priority="low"))
    owner.add_pet(pet)
    assert Scheduler(owner=owner).detect_conflicts() == []


# ── Edge cases ─────────────────────────────────────────────────────────────────

def test_generate_plan_with_no_tasks_returns_empty_plan():
    owner = Owner(name="Alex", available_time_per_day=60)
    owner.add_pet(Pet(name="Buddy", species="Dog", age=3))
    plan = Scheduler(owner=owner).generate_plan()
    assert plan.scheduled_tasks == []
    assert plan.total_duration == 0


def test_generate_plan_skips_tasks_exceeding_time_budget():
    owner = Owner(name="Alex", available_time_per_day=15)
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Long Walk", category="walk", duration=60, priority="high"))
    pet.add_task(Task(name="Quick Feed", category="feed", duration=10, priority="high"))
    owner.add_pet(pet)
    plan = Scheduler(owner=owner).generate_plan()
    names = [t.name for t in plan.scheduled_tasks]
    assert "Long Walk" not in names
    assert "Quick Feed" in names
