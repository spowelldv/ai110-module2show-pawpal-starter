"""Backend logic for PawPal+: owners, pets, tasks, and scheduling."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, List, Optional


def _today() -> date:
    """Used so tests can patch today's date without mocking the date class."""
    return date.today()


def _priority_rank(priority: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(priority.lower(), 2)


def _time_to_minutes(hhmm: str) -> int:
    parsed = datetime.strptime(hhmm, "%H:%M")
    return parsed.hour * 60 + parsed.minute


def _minutes_to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: date = field(default_factory=_today)
    pet_name: str = ""
    priority: str = "medium"
    duration_minutes: int = 30

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

    def save_to_json(self, path: str | Path) -> None:
        """Write owner, pets, and tasks to a JSON file."""
        path = Path(path)
        data: dict[str, Any] = {"name": self.name, "pets": []}
        for pet in self.pets:
            pdata = {
                "name": pet.name,
                "species": pet.species,
                "tasks": [_task_to_jsonable(t) for t in pet.tasks],
            }
            data["pets"].append(pdata)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def load_from_json(path: str | Path) -> Owner:
        """Load an Owner graph from JSON."""
        path = Path(path)
        raw = json.loads(path.read_text(encoding="utf-8"))
        owner = Owner(raw["name"])
        for p in raw.get("pets", []):
            pet = Pet(name=p["name"], species=p["species"])
            for td in p.get("tasks", []):
                pet.add_task(_task_from_jsonable(td))
            owner.add_pet(pet)
        return owner


def _task_to_jsonable(t: Task) -> dict[str, Any]:
    return {
        "description": t.description,
        "time": t.time,
        "frequency": t.frequency,
        "completed": t.completed,
        "due_date": t.due_date.isoformat(),
        "pet_name": t.pet_name,
        "priority": t.priority,
        "duration_minutes": t.duration_minutes,
    }


def _task_from_jsonable(d: dict[str, Any]) -> Task:
    return Task(
        description=d["description"],
        time=d["time"],
        frequency=d["frequency"],
        completed=d.get("completed", False),
        due_date=date.fromisoformat(d["due_date"]),
        pet_name=d.get("pet_name", ""),
        priority=d.get("priority", "medium"),
        duration_minutes=int(d.get("duration_minutes", 30)),
    )


class Scheduler:
    """Collects and organizes tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def tasks_for_today(self) -> List[Task]:
        """Return today's unfinished tasks, sorted by priority then time."""
        today = _today()
        tasks = [
            t
            for t in self.owner.all_tasks()
            if t.due_date == today and not t.completed
        ]
        return self.sort_by_priority_and_time(tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their time string (expects HH:MM)."""

        def time_key(task: Task) -> int:
            return _time_to_minutes(task.time)

        return sorted(tasks, key=time_key)

    def sort_by_priority_and_time(self, tasks: List[Task]) -> List[Task]:
        """Sort by priority (high first) then by time."""

        def key(task: Task) -> tuple[int, int]:
            return (-_priority_rank(task.priority), _time_to_minutes(task.time))

        return sorted(tasks, key=key)

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

    def weighted_score(self, task: Task) -> float:
        """Simple score: priority weight plus minute-of-day (lower time slightly favors earlier)."""
        p = _priority_rank(task.priority) * 1000.0
        m = _time_to_minutes(task.time) / (24 * 60.0)
        return p + (1.0 - m)

    def next_available_slot(
        self, after_time: str = "06:00", duration_minutes: int = 30
    ) -> Optional[str]:
        """First HH:MM today after after_time with no overlap with unfinished tasks (by duration)."""
        today = _today()
        tasks = [
            t
            for t in self.owner.all_tasks()
            if t.due_date == today and not t.completed
        ]
        intervals: List[tuple[int, int]] = []
        for t in tasks:
            s = _time_to_minutes(t.time)
            intervals.append((s, s + t.duration_minutes))
        intervals.sort()
        after_m = _time_to_minutes(after_time)
        day_end = 24 * 60
        for start in range(after_m, day_end - duration_minutes + 1):
            end = start + duration_minutes
            if not any(start < b and end > a for a, b in intervals):
                return _minutes_to_hhmm(start)
        return None

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
                    priority=task.priority,
                    duration_minutes=task.duration_minutes,
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
                    priority=task.priority,
                    duration_minutes=task.duration_minutes,
                )
            )
