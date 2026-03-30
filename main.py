from datetime import date

from tabulate import tabulate

from pawpal_system import Owner, Pet, Scheduler, Task


def priority_label(p: str) -> str:
    return {"high": "high", "medium": "med", "low": "low"}.get(p.lower(), p)


def print_schedule(label: str, tasks: list[Task]) -> None:
    print(label)
    rows = []
    for task in tasks:
        status = "done" if task.completed else "todo"
        pet = task.pet_name or "?"
        rows.append(
            [
                task.time,
                priority_label(task.priority),
                task.duration_minutes,
                task.description,
                task.frequency,
                pet,
                str(task.due_date),
                status,
            ]
        )
    print(
        tabulate(
            rows,
            headers=["Time", "Pri", "Min", "Task", "Freq", "Pet", "Due", "Status"],
            tablefmt="simple",
        )
    )
    print()


def main() -> None:
    today = date.today()

    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(
        Task(
            description="Breakfast",
            time="08:00",
            frequency="daily",
            due_date=today,
            priority="low",
            duration_minutes=15,
        )
    )
    luna.add_task(
        Task(
            description="Medication",
            time="07:45",
            frequency="daily",
            due_date=today,
            priority="high",
            duration_minutes=10,
        )
    )
    mochi.add_task(
        Task(
            description="Morning walk",
            time="07:30",
            frequency="daily",
            due_date=today,
            priority="medium",
            duration_minutes=30,
        )
    )

    mochi.add_task(
        Task(
            description="Brush teeth",
            time="08:00",
            frequency="once",
            due_date=today,
            priority="low",
            duration_minutes=5,
        )
    )
    luna.add_task(
        Task(
            description="Play session",
            time="08:00",
            frequency="once",
            due_date=today,
            priority="medium",
            duration_minutes=20,
        )
    )

    scheduler = Scheduler(owner)

    print_schedule("Today's schedule (priority, then time)", scheduler.tasks_for_today())

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

    slot = scheduler.next_available_slot(after_time="07:00", duration_minutes=25)
    print("Next 25-minute slot after 07:00 (today):", slot or "none found")
    print()

    daily = mochi.tasks[0]
    scheduler.mark_task_complete(mochi, daily)
    print("After marking Breakfast complete (daily), Mochi's tasks:")
    print("-" * 40)
    for task in mochi.tasks:
        status = "done" if task.completed else "todo"
        print(
            f"{task.time}  {priority_label(task.priority)}  {task.description}  "
            f"({task.frequency})  due {task.due_date}  [{status}]"
        )


if __name__ == "__main__":
    main()
