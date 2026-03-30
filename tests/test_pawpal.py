from datetime import date
from unittest.mock import patch

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_sets_completed_true() -> None:
    task = Task(description="Test task", time="09:00", frequency="once")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_task_count_and_sets_pet_name() -> None:
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Walk", time="07:30", frequency="daily"))
    assert len(pet.tasks) == 1
    assert pet.tasks[0].pet_name == "Mochi"


def test_sort_by_time_returns_chronological_order() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 3, 30)
    pet.add_task(Task(description="Late", time="10:00", frequency="daily", due_date=d))
    pet.add_task(Task(description="Early", time="07:00", frequency="daily", due_date=d))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time(owner.all_tasks())
    assert [t.time for t in ordered] == ["07:00", "10:00"]


def test_daily_mark_complete_creates_next_day_task() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 3, 30)
    walk = Task(description="Walk", time="07:00", frequency="daily", due_date=d)
    pet.add_task(walk)

    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(pet, walk)

    assert walk.completed is True
    assert len(pet.tasks) == 2
    next_task = [t for t in pet.tasks if t is not walk][0]
    assert next_task.due_date == date(2026, 3, 31)
    assert next_task.completed is False


def test_detect_conflicts_flags_same_time() -> None:
    owner = Owner("Jordan")
    a = Pet(name="Mochi", species="dog")
    b = Pet(name="Luna", species="cat")
    owner.add_pet(a)
    owner.add_pet(b)
    d = date(2026, 4, 1)
    a.add_task(Task(description="One", time="09:00", frequency="once", due_date=d))
    b.add_task(Task(description="Two", time="09:00", frequency="once", due_date=d))

    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
