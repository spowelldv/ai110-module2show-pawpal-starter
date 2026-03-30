from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(tasks: list[Task]) -> None:
    print("Today's Schedule")
    print("-" * 40)
    for task in tasks:
        status = "done" if task.completed else "todo"
        print(f"{task.time}  {task.description}  ({task.frequency})  [{status}]")


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task(description="Morning walk", time="07:30", frequency="daily"))
    mochi.add_task(Task(description="Breakfast", time="08:00", frequency="daily"))
    luna.add_task(Task(description="Medication", time="07:45", frequency="daily"))

    scheduler = Scheduler(owner)
    schedule = scheduler.tasks_for_today()
    print_schedule(schedule)


if __name__ == "__main__":
    main()

