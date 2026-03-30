from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(label: str, tasks: list[Task]) -> None:
    print(label)
    print("-" * 40)
    for task in tasks:
        status = "done" if task.completed else "todo"
        pet = task.pet_name or "?"
        print(
            f"{task.time}  {task.description}  ({task.frequency})  "
            f"[{pet}]  due {task.due_date}  [{status}]"
        )
    print()


def main() -> None:
    today = date.today()

    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of order on purpose (scheduler sorts by time)
    mochi.add_task(
        Task(description="Breakfast", time="08:00", frequency="daily", due_date=today)
    )
    luna.add_task(
        Task(description="Medication", time="07:45", frequency="daily", due_date=today)
    )
    mochi.add_task(
        Task(description="Morning walk", time="07:30", frequency="daily", due_date=today)
    )

    # Same time on purpose (conflict warning)
    mochi.add_task(
        Task(description="Brush teeth", time="08:00", frequency="once", due_date=today)
    )
    luna.add_task(
        Task(description="Play session", time="08:00", frequency="once", due_date=today)
    )

    scheduler = Scheduler(owner)

    print_schedule("Today's schedule (sorted by time)", scheduler.tasks_for_today())

    unfinished = scheduler.filter_tasks(completed=False)
    print_schedule("All unfinished tasks (any due date)", unfinished)

    conflicts = scheduler.detect_conflicts()
    print("Conflict warnings")
    print("-" * 40)
    if conflicts:
        for line in conflicts:
            print(line)
    else:
        print("None")
    print()

    daily = mochi.tasks[0]
    scheduler.mark_task_complete(mochi, daily)
    print("After marking Breakfast complete (daily), Mochi's tasks:")
    print("-" * 40)
    for task in mochi.tasks:
        status = "done" if task.completed else "todo"
        print(
            f"{task.time}  {task.description}  ({task.frequency})  "
            f"due {task.due_date}  [{status}]"
        )


if __name__ == "__main__":
    main()
