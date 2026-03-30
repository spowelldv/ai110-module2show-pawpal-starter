PawPal+ Project Reflection

1. System Design

A user should be able to add their pets with basic info like name and species so the app knows who needs care. They should be able to schedule care tasks such as walks, feeding, or meds with a time and how often each task repeats. They should also be able to see what is due today in a clear order so nothing important gets skipped.

a. Initial design

The design uses four main classes. Task is one activity. It has a description, a time, how often it happens, and whether it is finished, and there is a way to mark it complete. Pet has a name, a species, and a list of tasks, and you can add tasks to a pet. Owner has a name and a list of pets, and can add pets and pull together all tasks from every pet. Scheduler works with an owner. It will list tasks for today and sort them by time once the logic is written.

b. Design changes

I ended up adding a due date on each task and a pet name on each task so the scheduler can tell what is due today and filter by pet without guessing. I also added real methods on the scheduler for filtering, conflicts, and rolling daily or weekly tasks forward when you mark one done. That is more than the first skeleton but it still matches the same four classes, just with more detail filled in.

2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

The scheduler mostly cares about the clock time on each task so it can sort in order. It also uses a due date so “today” only pulls tasks that are actually due today and not finished yet. Filtering can narrow by whether something is done or which pet it belongs to. I did not build priority levels yet, so if two things clash the app just warns about the time overlap instead of picking a winner.

b. Tradeoffs

Conflict checking only looks at the exact same time string, not how long a task might run, so two things could still overlap in real life if one is long and the next starts before the first really ends. That is a tradeoff I kept on purpose because it keeps the first version simple and still catches the obvious double booking case when two tasks start at the same minute.

3. AI Collaboration

a. How you used AI

I used Cursor with Claude to help scaffold classes, wire Streamlit session state, and write tests when I got stuck on edge cases. The prompts that worked best were the ones where I pasted the exact file or error and asked for a small change, not a whole rewrite.

b. Judgment and verification

Sometimes the model wanted to add extra features or refactor everything at once. I did not always take that. I kept the model focused on one behavior at a time and I checked it by running the demo script and the tests so I could see if the behavior was really right.

4. Testing and Verification

a. What you tested

I tested marking tasks complete, adding tasks to pets, sorting by time, daily and weekly follow-up tasks, conflict warnings when two tasks share a time, empty lists, filtering by pet, and a case where there should be no conflict. Those tests matter because they are the main ways this app can break in real use.

b. Confidence

I feel pretty good, maybe a 4 out of 5. If I had more time I would test bad time formats, duplicate pets with the same name, and longer tasks that overlap in real minutes even when the start times differ.

5. Reflection

a. What went well

The part I like most is that the same Owner object stays in Streamlit session state, so the app actually feels like one connected system instead of fake lists that reset.

b. What you would improve

I would add real priority levels and maybe duration so conflicts could mean more than the same start minute. I would also make the UI a little nicer for editing or deleting a task.

c. Key takeaway

The important lesson for me is that I still have to be the one deciding what belongs in scope. The AI can write a lot of code fast, but I have to say what done means and check it.
