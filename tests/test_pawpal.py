from datetime import date
from unittest.mock import patch

from pawpal_system import Owner, Pet, Scheduler, Task, parse_hhmm


def test_task_mark_complete_sets_completed_true() -> None:
    task = Task(description="Test task", time="09:00", frequency="once")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_parse_hhmm_valid_and_invalid() -> None:
    assert parse_hhmm("09:00") == "09:00"
    assert parse_hhmm("  14:30  ") == "14:30"
    assert parse_hhmm("25:00") is None
    assert parse_hhmm("9:00") == "09:00"
    assert parse_hhmm("not-a-time") is None


def test_pet_remove_task() -> None:
    pet = Pet(name="Mochi", species="dog")
    t = Task(description="Walk", time="08:00", frequency="daily")
    pet.add_task(t)
    assert pet.remove_task(t) is True
    assert pet.tasks == []
    assert pet.remove_task(t) is False


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


def test_tasks_for_today_empty_when_pet_has_no_tasks() -> None:
    owner = Owner("Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog"))
    with patch("pawpal_system._today", return_value=date(2026, 6, 1)):
        scheduler = Scheduler(owner)
        assert scheduler.tasks_for_today() == []


def test_tasks_for_today_skips_completed() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 6, 15)
    t = Task(description="Walk", time="08:00", frequency="daily", completed=True, due_date=d)
    pet.add_task(t)
    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        assert scheduler.tasks_for_today() == []


def test_weekly_mark_complete_creates_task_one_week_out() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 7, 1)
    vet = Task(description="Vet check", time="14:00", frequency="weekly", due_date=d)
    pet.add_task(vet)

    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(pet, vet)

    assert vet.completed is True
    nxt = [x for x in pet.tasks if x is not vet][0]
    assert nxt.due_date == date(2026, 7, 8)


def test_filter_tasks_by_pet_name() -> None:
    owner = Owner("Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    d = date(2026, 8, 1)
    mochi.add_task(Task(description="A", time="09:00", frequency="daily", due_date=d))
    luna.add_task(Task(description="B", time="10:00", frequency="daily", due_date=d))

    scheduler = Scheduler(owner)
    only_mochi = scheduler.filter_tasks(pet_name="Mochi")
    assert len(only_mochi) == 1
    assert only_mochi[0].description == "A"


def test_no_conflict_when_times_differ() -> None:
    owner = Owner("Jordan")
    a = Pet(name="Mochi", species="dog")
    b = Pet(name="Luna", species="cat")
    owner.add_pet(a)
    owner.add_pet(b)
    d = date(2026, 9, 1)
    a.add_task(Task(description="One", time="09:00", frequency="once", due_date=d))
    b.add_task(Task(description="Two", time="10:00", frequency="once", due_date=d))

    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        assert scheduler.detect_conflicts() == []


def test_tasks_for_today_sorts_priority_then_time() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 10, 15)
    pet.add_task(
        Task(description="Early low", time="08:00", frequency="daily", due_date=d, priority="low")
    )
    pet.add_task(
        Task(description="Late high", time="10:00", frequency="daily", due_date=d, priority="high")
    )
    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        ordered = scheduler.tasks_for_today()
    assert [t.description for t in ordered] == ["Late high", "Early low"]


def test_save_and_load_json_roundtrip(tmp_path) -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(
        Task(
            description="Walk",
            time="09:00",
            frequency="daily",
            due_date=date(2026, 11, 1),
            priority="high",
            duration_minutes=45,
        )
    )
    path = tmp_path / "data.json"
    owner.save_to_json(path)
    owner2 = Owner.load_from_json(path)
    assert owner2.name == "Jordan"
    assert owner2.pets[0].name == "Mochi"
    t = owner2.pets[0].tasks[0]
    assert t.description == "Walk"
    assert t.priority == "high"
    assert t.duration_minutes == 45


def test_next_available_slot_finds_gap() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    d = date(2026, 12, 1)
    pet.add_task(
        Task(description="A", time="09:00", frequency="once", due_date=d, duration_minutes=60)
    )
    with patch("pawpal_system._today", return_value=d):
        scheduler = Scheduler(owner)
        slot = scheduler.next_available_slot(after_time="07:00", duration_minutes=30)
    assert slot == "07:00"
