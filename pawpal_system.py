"""Backend logic for PawPal+: owners, pets, tasks, and scheduling."""

from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: str
    frequency: str
    completed: bool = False

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
        """Return today's tasks (basic version: all tasks, sorted by time)."""
        return self.sort_by_time(self.owner.all_tasks())

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their time string (expects HH:MM)."""

        def time_key(task: Task) -> int:
            parsed = datetime.strptime(task.time, "%H:%M")
            return parsed.hour * 60 + parsed.minute

        return sorted(tasks, key=time_key)
