"""Backend logic for PawPal+: owners, pets, tasks, and scheduling."""

from __future__ import annotations

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
        pass


@dataclass
class Pet:
    """A pet and the tasks assigned to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


class Owner:
    """Someone who has one or more pets."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    """Collects and organizes tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def tasks_for_today(self) -> List[Task]:
        pass

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        pass
