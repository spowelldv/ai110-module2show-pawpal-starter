from pawpal_system import Pet, Task


def test_task_mark_complete_sets_completed_true() -> None:
    task = Task(description="Test task", time="09:00", frequency="once")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Walk", time="07:30", frequency="daily"))
    assert len(pet.tasks) == 1

