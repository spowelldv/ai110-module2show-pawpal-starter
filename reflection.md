PawPal+ Project Reflection

1. System Design

A user should be able to add their pets with basic info like name and species so the app knows who needs care. They should be able to schedule care tasks such as walks, feeding, or meds with a time and how often each task repeats. They should also be able to see what is due today in a clear order so nothing important gets skipped.

a. Initial design

The design uses four main classes. Task is one activity. It has a description, a time, how often it happens, and whether it is finished, and there is a way to mark it complete. Pet has a name, a species, and a list of tasks, and you can add tasks to a pet. Owner has a name and a list of pets, and can add pets and pull together all tasks from every pet. Scheduler works with an owner. It will list tasks for today and sort them by time once the logic is written.

b. Design changes

The code ended up with more than the first skeleton. Tasks now have a due date and a pet name on them. The scheduler can filter tasks, warn about time conflicts, and when you finish a daily or weekly task it creates the next one on the right date. After that I also added priority, how many minutes a task takes, saving the owner to a json file, and a small helper that looks for the next open time slot. I did most of that with AI in Cursor, then I ran main.py and pytest to check that it actually worked.

2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

For today’s list it sorts by priority first, then by time. It only pulls tasks that are due today and not done yet. You can filter by whether a task is done or by which pet it belongs to. If two tasks start at the same time you get a warning so you know about it.

b. Tradeoffs

Conflicts are only about the same start time, not two tasks that overlap because one runs long. The next-slot helper does use how long each task takes when it looks for a free gap, so that part is a little smarter, but it is still a simple scheduler for this project, not something like Google Calendar.

3. AI Collaboration

a. How you used AI

I used Cursor with AI help for a lot of the project: the class layout, pawpal_system.py, Streamlit, tests, and the extra features at the end. What worked for me was running pytest and main.py after changes and asking for fixes when something broke or looked wrong, instead of trusting the first answer every time.

b. Judgment and verification

I did not use every suggestion as-is. Sometimes it wanted to change too much at once or add things I did not need for the assignment. I tried to stay close to what the course asked for. I used tests and the CLI demo to see if things behaved right, and I read enough of the code to explain it myself.

4. Testing and Verification

a. What you tested

The tests check marking tasks done, adding tasks, sorting, daily and weekly repeats, conflicts, empty cases, filtering, priority order, saving and loading json, and the next-slot helper. Some of those tests were written with AI help. I ran them a lot while I was building and again before I turned it in.

b. Confidence

I feel okay about it, maybe a 4 out of 5 for the stuff the tests actually cover. I did not dig much into bad time input, two pets with the same name, or weird times around midnight.

5. Reflection

a. What went well

I like that the owner stays in session state in Streamlit, and that I can save to a file so everything is not gone every time I refresh, as long as I saved.

b. What you would improve

I would add a way to edit or delete tasks in the app, and I would check time input more carefully so garbage strings do not slip through. I might also simplify how the page looks so it is easier to read.

c. Key takeaway

AI can write code fast, but I still have to make sure it matches the assignment, runs, and that I understand it well enough to talk about it.

6. Prompt comparison (optional extension)

I did not run the same prompt in two different chat apps for this class. I built the next-slot part and the rest of the extras in Cursor like the rest of the project. If I had to compare two models for real, I would pick one function, give both the same instructions, and see which answer I could drop into my code and test more easily.
