"""Backend logic for PawPal+: owners, pets, tasks, and scheduling."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


def _today() -> date:
    """Used so tests can patch today's date without mocking the date class."""
    return date.today()


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: date = field(default_factory=_today)
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the tasks assigned to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)


class Owner:
    """Someone who has one or more pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> List[Task]:
        """Return a flat list of tasks across all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Collects and organizes tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def tasks_for_today(self) -> List[Task]:
        """Return today's unfinished tasks, sorted by time."""
        today = _today()
        tasks = [
            t
            for t in self.owner.all_tasks()
            if t.due_date == today and not t.completed
        ]
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their time string (expects HH:MM)."""

        def time_key(task: Task) -> int:
            parsed = datetime.strptime(task.time, "%H:%M")
            return parsed.hour * 60 + parsed.minute

        return sorted(tasks, key=time_key)

    def filter_tasks(
        self, completed: Optional[bool] = None, pet_name: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by completion and/or pet name."""
        out = list(self.owner.all_tasks())
        if completed is not None:
            out = [t for t in out if t.completed == completed]
        if pet_name:
            out = [t for t in out if t.pet_name == pet_name]
        return out

    def detect_conflicts(self) -> List[str]:
        """Return warning strings when two or more unfinished tasks share the same time today."""
        today = _today()
        tasks = [
            t
            for t in self.owner.all_tasks()
            if t.due_date == today and not t.completed
        ]
        by_time: dict[str, List[Task]] = defaultdict(list)
        for t in tasks:
            by_time[t.time].append(t)
        warnings: List[str] = []
        for time_str, group in by_time.items():
            if len(group) > 1:
                detail = ", ".join(f"{x.pet_name}: {x.description}" for x in group)
                warnings.append(f"Conflict at {time_str}: {detail}")
        return warnings

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Mark a task done; daily/weekly tasks get a new instance for the next due date."""
        task.mark_complete()
        if task.frequency == "daily":
            next_due = _today() + timedelta(days=1)
            pet.add_task(
                Task(
                    description=task.description,
                    time=task.time,
                    frequency=task.frequency,
                    due_date=next_due,
                )
            )
        elif task.frequency == "weekly":
            next_due = _today() + timedelta(days=7)
            pet.add_task(
                Task(
                    description=task.description,
                    time=task.time,
                    frequency=task.frequency,
                    due_date=next_due,
                )
            )
