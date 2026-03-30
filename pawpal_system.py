from dataclasses import dataclass, field
from datetime import date as today_date, timedelta
from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single pet care activity."""
    name: str
    category: str
    duration: int
    priority: str
    is_completed: bool = False
    frequency: str = "once"          # "once", "daily", or "weekly"
    due_date: Optional[str] = None   # "YYYY-MM-DD"; None means no specific due date
    start_time: Optional[str] = None # "HH:MM" used for sort_by_time

    def mark_complete(self) -> None:
        """Mark this task as completed and schedule the next occurrence for recurring tasks."""
        self.is_completed = True
        if self.frequency == "daily":
            self.due_date = str(today_date.today() + timedelta(days=1))
            self.is_completed = False
        elif self.frequency == "weekly":
            self.due_date = str(today_date.today() + timedelta(weeks=1))
            self.is_completed = False

    def update(self, **kwargs) -> None:
        """Update any task field by keyword argument (e.g. update(priority='high'))."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class Pet:
    """Stores pet details and owns a list of care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted string with the pet's name, species, and age."""
        return f"{self.name} ({self.species}, age {self.age})"

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task from this pet's task list by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]


class Owner:
    """Manages one or more pets and provides access to all their tasks."""

    def __init__(self, name: str, available_time_per_day: int, preferences: str = ""):
        self.name = name
        self.available_time_per_day = available_time_per_day  
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_available_time(self) -> int:
        """Return the owner's daily time budget in minutes."""
        return self.available_time_per_day

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's scheduling preferences."""
        self.preferences = preferences

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet this owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The brain that retrieves, organizes, and schedules tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by start_time in HH:MM format; tasks without a time go last."""
        def time_key(t: Task) -> str:
            return t.start_time if t.start_time else "99:99"
        return sorted(tasks, key=lambda t: time_key(t))

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        results = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if completed is not None and task.is_completed != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any two tasks that share the same start_time."""
        timed = [t for t in self.owner.get_all_tasks() if t.start_time and not t.is_completed]
        seen: dict = {}
        warnings = []
        for task in timed:
            if task.start_time in seen:
                warnings.append(
                    f"Conflict at {task.start_time}: '{seen[task.start_time]}' and '{task.name}' overlap."
                )
            else:
                seen[task.start_time] = task.name
        return warnings

    def prioritize_tasks(self) -> List[Task]:
        """Sort all pending tasks by priority (high → medium → low), then duration (shortest first)."""
        pending = [t for t in self.owner.get_all_tasks() if not t.is_completed]
        return sorted(pending, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration))

    def check_constraints(self) -> List[str]:
        """Return a list of constraint warnings (empty means all clear)."""
        warnings = []
        total = sum(t.duration for t in self.owner.get_all_tasks() if not t.is_completed)
        available = self.owner.get_available_time()
        if total > available:
            warnings.append(
                f"Total task time ({total} min) exceeds available time ({available} min)."
            )
        if not self.owner.pets:
            warnings.append("No pets registered for this owner.")
        return warnings

    def generate_plan(self) -> "DailyPlan":
        """Greedily schedule tasks by priority until time budget is used up."""
        available = self.owner.get_available_time()
        prioritized = self.prioritize_tasks()

        scheduled = []
        total_duration = 0
        skipped = []

        for task in prioritized:
            if total_duration + task.duration <= available:
                scheduled.append(task)
                total_duration += task.duration
            else:
                skipped.append(task.name)

        explanation_parts = [
            f"Scheduled {len(scheduled)} task(s) totalling {total_duration} of {available} available minutes.",
            "Tasks were ordered by priority (high → medium → low), then shortest duration first.",
        ]
        if skipped:
            explanation_parts.append(f"Skipped due to time limit: {', '.join(skipped)}.")

        return DailyPlan(
            date=str(today_date.today()),
            scheduled_tasks=scheduled,
            total_duration=total_duration,
            explanation=" ".join(explanation_parts),
        )


class DailyPlan:
    """Stores and displays the generated daily care schedule."""

    def __init__(self, date: str, scheduled_tasks: List[Task], total_duration: int, explanation: str):
        self.date = date
        self.scheduled_tasks = scheduled_tasks
        self.total_duration = total_duration
        self.explanation = explanation

    def display(self) -> None:
        """Print the full daily schedule with task details and reasoning to the terminal."""
        print(f"\n--- Daily Plan for {self.date} ---")
        for i, task in enumerate(self.scheduled_tasks, 1):
            status = "done" if task.is_completed else "pending"
            print(f"  {i}. [{task.priority.upper()}] {task.name} ({task.category}) — {task.duration} min [{status}]")
        print(f"Total: {self.total_duration} min")
        print(f"Reasoning: {self.explanation}\n")

    def get_summary(self) -> str:
        """Return a one-line summary string of the plan."""
        names = ", ".join(t.name for t in self.scheduled_tasks)
        return f"{self.date}: {len(self.scheduled_tasks)} tasks scheduled ({self.total_duration} min) — {names}"
