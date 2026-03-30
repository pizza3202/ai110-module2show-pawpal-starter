from dataclasses import dataclass, field
from typing import List, Optional


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences: str = ""):
        self.name = name
        self.available_time_per_day = available_time_per_day  # in minutes
        self.preferences = preferences

    def get_available_time(self) -> int:
        pass

    def update_preferences(self, preferences: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    owner: Optional[Owner] = None

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    name: str
    category: str          # e.g. "walk", "feed", "medication", "grooming", "enrichment"
    duration: int          # in minutes
    priority: str          # "high", "medium", or "low"
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass

    def update(self, **kwargs) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def generate_plan(self) -> "DailyPlan":
        pass

    def prioritize_tasks(self) -> List[Task]:
        pass

    def check_constraints(self) -> bool:
        pass


class DailyPlan:
    def __init__(self, date: str, scheduled_tasks: List[Task], total_duration: int, explanation: str):
        self.date = date
        self.scheduled_tasks = scheduled_tasks
        self.total_duration = total_duration
        self.explanation = explanation

    def display(self) -> None:
        pass

    def get_summary(self) -> str:
        pass
