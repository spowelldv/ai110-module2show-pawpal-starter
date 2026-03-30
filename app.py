import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

st.title("PawPal+")

st.markdown(
    "Plan care for your pets. Add pets and tasks below, then build today’s schedule using your scheduler."
)

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name.strip() or owner.name

st.divider()

st.subheader("Add a pet")
pc1, pc2 = st.columns(2)
with pc1:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with pc2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_species")

if st.button("Add pet"):
    name = new_pet_name.strip()
    if name:
        owner.add_pet(Pet(name=name, species=new_species))
        st.success(f"Added {name}.")
    else:
        st.warning("Enter a pet name.")

if owner.pets:
    st.caption("Your pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a task")
if not owner.pets:
    st.caption("Add a pet first so you can attach tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    task_pet = st.selectbox("Pet", pet_names, key="task_pet")
    t1, t2, t3 = st.columns(3)
    with t1:
        task_desc = st.text_input("What to do", value="Morning walk", key="task_desc")
    with t2:
        task_time = st.text_input("Time (HH:MM)", value="09:00", key="task_time")
    with t3:
        task_freq = st.selectbox("How often", ["daily", "weekly", "once"], key="task_freq")

    if st.button("Add task"):
        desc = task_desc.strip()
        if not desc:
            st.warning("Enter what to do.")
        else:
            pet = next(p for p in owner.pets if p.name == task_pet)
            pet.add_task(Task(description=desc, time=task_time.strip(), frequency=task_freq))
            st.success("Task added.")

st.divider()

st.subheader("Today’s schedule")
st.caption("Uses Scheduler to sort tasks by time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.tasks_for_today()
    if not schedule:
        st.info("No tasks yet. Add tasks above.")
    else:
        rows = []
        for t in schedule:
            rows.append(
                {
                    "Time": t.time,
                    "Task": t.description,
                    "Frequency": t.frequency,
                    "Done": "yes" if t.completed else "no",
                }
            )
        st.table(rows)
