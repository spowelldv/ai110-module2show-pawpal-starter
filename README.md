PawPal+ (Module 2 Project)

This project is a Streamlit app that helps a pet owner plan care tasks for their pets.

Scenario

A busy pet owner needs to stay consistent with pet care. They want to track tasks like walks, feeding, and meds, work within time and preferences, and get a clear daily plan.

You design the system, implement the logic in Python, then connect it to Streamlit.

Features

The owner can have more than one pet. Each pet has a name, species, and a list of tasks. Each task has a short description, a clock time in HH:MM form, how often it repeats (daily, weekly, or once), a due date, and whether it is done.

The scheduler sorts by time, can filter by done or not done or by pet name, warns when two unfinished tasks today start at the same time, and when you finish a daily or weekly task it adds the next occurrence on a new due date.

The Streamlit app keeps the owner in session state, shows today’s schedule and conflict warnings, and lets you mark tasks done on the same page.

Smarter scheduling

Sorting, filtering, conflict warnings, and rolling daily or weekly tasks forward when you mark them complete are all implemented in pawpal_system.py and used from the app.

Testing PawPal+

From the project folder (activate your venv first if you use one):

```
python -m pytest
```

The tests cover marking tasks complete, adding tasks to pets, sorting by time, daily and weekly follow-up tasks, conflicts when two tasks share a time, empty schedules, filtering by pet, and a case with no conflict.

I would rate my confidence around 4 out of 5 for normal use. Conflict checks only look at the same start time, not overlapping durations, and times need to stay in HH:MM format.

Demo

Run the app with:

```
streamlit run app.py
```

Screenshot of the running app:

![PawPal+ app](pawpal_demo.png)

UML

The Mermaid source for the class diagram is in uml_final.mmd. The exported image is uml_final.png.

Getting started

Setup:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows use .venv\Scripts\activate instead of source.

Suggested workflow: read the scenario, sketch UML, add class stubs, implement scheduling in small steps, add tests, connect app.py, then align the diagram with the final code.
