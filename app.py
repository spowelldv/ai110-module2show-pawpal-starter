from pathlib import Path

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

DATA_FILE = Path("data.json")


def priority_cell(p: str) -> str:
    return {
        "high": "High",
        "medium": "Med",
        "low": "Low",
    }.get(p.lower(), p)


def load_owner() -> Owner:
    if DATA_FILE.exists():
        return Owner.load_from_json(DATA_FILE)
    return Owner("Jordan")


def save_owner(owner: Owner) -> None:
    owner.save_to_json(DATA_FILE)


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.markdown(
    """
<style>
:root {
  --apple-text: #1d1d1f;
  --apple-secondary: #86868b;
  --apple-bg: #f5f5f7;
  --apple-surface: #ffffff;
  --apple-line: #d2d2d7;
  --apple-blue: #0071e3;
  --apple-blue-hover: #0077ed;
}

html, body, [class*="css"] {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  color: var(--apple-text);
}

.stApp {
  background: var(--apple-bg);
}

.block-container {
  max-width: 692px;
  padding-top: 2.5rem;
  padding-bottom: 4rem;
}

.apple-hero {
  text-align: center;
  padding: 2.5rem 1rem 2rem 1rem;
  margin-bottom: 0.5rem;
}
.apple-hero h1 {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 600;
  letter-spacing: -0.022em;
  color: var(--apple-text);
  margin: 0 0 0.6rem 0;
  line-height: 1.05;
}
.apple-hero .subtitle {
  font-size: 1.125rem;
  line-height: 1.47;
  color: var(--apple-secondary);
  margin: 0 auto;
  max-width: 36rem;
  font-weight: 400;
}

h3 {
  font-size: 1.5rem !important;
  font-weight: 600 !important;
  letter-spacing: -0.015em !important;
  color: var(--apple-text) !important;
  margin: 1.75rem 0 0.75rem 0 !important;
}

[data-testid="stCaption"] {
  color: var(--apple-secondary) !important;
  font-size: 0.875rem !important;
}

hr {
  margin: 1.5rem 0 !important;
  border: none !important;
  border-top: 1px solid var(--apple-line) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
  border-radius: 10px !important;
  border-color: var(--apple-line) !important;
}

.stButton > button[kind="primary"] {
  background-color: var(--apple-blue) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 980px !important;
  font-weight: 500 !important;
  font-size: 0.9375rem !important;
  padding: 0.55rem 1.35rem !important;
  min-height: 2.75rem !important;
}
.stButton > button[kind="primary"]:hover {
  background-color: var(--apple-blue-hover) !important;
}

.stButton > button[kind="secondary"] {
  border-radius: 980px !important;
  font-weight: 500 !important;
  border: 1px solid var(--apple-line) !important;
  color: var(--apple-text) !important;
  background: var(--apple-surface) !important;
}

[data-testid="stTable"] {
  border: 1px solid var(--apple-line) !important;
  border-radius: 12px !important;
  overflow: hidden;
}
[data-testid="stTable"] th {
  background: #fafafa !important;
  color: var(--apple-text) !important;
  font-weight: 600 !important;
  font-size: 0.8125rem !important;
}
[data-testid="stTable"] td {
  font-size: 0.875rem !important;
}

[data-testid="stAlert"] {
  border-radius: 12px !important;
  border: 1px solid var(--apple-line) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

if "owner" not in st.session_state:
    st.session_state.owner = load_owner()
    st.session_state.loaded_file = DATA_FILE.exists()

owner = st.session_state.owner

st.markdown(
    """
<div class="apple-hero">
  <h1>PawPal+</h1>
  <p class="subtitle">Plan care for your pets. Data saves to data.json in this folder when you add tasks or click save.</p>
</div>
""",
    unsafe_allow_html=True,
)

if st.session_state.get("loaded_file"):
    st.caption("Loaded saved data from data.json.")
    st.session_state.loaded_file = False

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name.strip() or owner.name

c1, c2 = st.columns(2)
with c1:
    if st.button("Save data to file", type="primary", use_container_width=True):
        save_owner(owner)
        st.success("Saved to data.json.")
with c2:
    if st.button("Clear saved file (fresh start)", use_container_width=True):
        if DATA_FILE.exists():
            DATA_FILE.unlink()
        st.session_state.owner = Owner("Jordan")
        st.rerun()

st.divider()

st.subheader("Add a pet")
pc1, pc2 = st.columns(2)
with pc1:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with pc2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_species")

if st.button("Add pet", type="primary", use_container_width=True):
    name = new_pet_name.strip()
    if name:
        owner.add_pet(Pet(name=name, species=new_species))
        save_owner(owner)
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
    t1, t2 = st.columns(2)
    with t1:
        task_desc = st.text_input("What to do", value="Morning walk", key="task_desc")
    with t2:
        task_time = st.text_input("Time (HH:MM)", value="09:00", key="task_time")
    t3, t4, t5 = st.columns(3)
    with t3:
        task_freq = st.selectbox("How often", ["daily", "weekly", "once"], key="task_freq")
    with t4:
        task_pri = st.selectbox("Priority", ["low", "medium", "high"], index=1, key="task_pri")
    with t5:
        task_dur = st.number_input("Minutes", min_value=5, max_value=240, value=30, step=5, key="task_dur")

    if st.button("Add task", type="primary", use_container_width=True):
        desc = task_desc.strip()
        if not desc:
            st.warning("Enter what to do.")
        else:
            pet = next(p for p in owner.pets if p.name == task_pet)
            pet.add_task(
                Task(
                    description=desc,
                    time=task_time.strip(),
                    frequency=task_freq,
                    priority=task_pri,
                    duration_minutes=int(task_dur),
                )
            )
            save_owner(owner)
            st.success("Task added.")

st.divider()

st.subheader("Today’s schedule")
st.caption("Sorted by priority, then time. Conflicts show as warnings.")

scheduler = Scheduler(owner)
slot_after = st.text_input("Next slot search: after time", value="07:00", key="slot_after")
slot_len = st.number_input("Slot length (minutes)", min_value=15, max_value=120, value=30, step=5, key="slot_len")
ns = scheduler.next_available_slot(after_time=slot_after.strip(), duration_minutes=int(slot_len))
st.caption("Next open slot for that length: " + (ns or "none in the rest of the day"))

if st.button("Generate schedule", type="primary", use_container_width=True):
    schedule = scheduler.tasks_for_today()
    warnings = scheduler.detect_conflicts()
    for w in warnings:
        st.warning(w)
    if not schedule:
        st.info("No tasks due today yet, or everything is done. Add tasks above.")
    else:
        rows = []
        for t in schedule:
            rows.append(
                {
                    "Pri": priority_cell(t.priority),
                    "Time": t.time,
                    "Min": t.duration_minutes,
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Frequency": t.frequency,
                    "Due": str(t.due_date),
                    "Done": "yes" if t.completed else "no",
                }
            )
        st.table(rows)
        st.success("Schedule uses priority first, then time of day.")

st.divider()

st.subheader("Mark tasks done today")
st.caption(
    "Daily and weekly tasks get the next due date when you mark them complete."
)
due = scheduler.tasks_for_today()
if not owner.pets:
    st.caption("Add a pet and tasks first.")
elif not due:
    st.info("Nothing left to do today that is still open, or nothing is due today.")
else:
    for i, task in enumerate(due):
        label = f"{task.time}  {priority_cell(task.priority)}  {task.pet_name}  {task.description}  ({task.frequency})"
        txt_col, btn_col = st.columns([4, 1])
        with txt_col:
            st.write(label)
        with btn_col:
            if st.button("Done", key=f"done_{i}", type="secondary"):
                pet = next(p for p in owner.pets if p.name == task.pet_name)
                scheduler.mark_task_complete(pet, task)
                save_owner(owner)
                st.rerun()
