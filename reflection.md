PawPal+ Project Reflection

1. System Design

A user should be able to add their pets with basic info like name and species so the app knows who needs care. They should be able to schedule care tasks such as walks, feeding, or meds with a time and how often each task repeats. They should also be able to see what is due today in a clear order so nothing important gets skipped.

a. Initial design

The design uses four main classes. Task is one activity. It has a description, a time, how often it happens, and whether it is finished, and there is a way to mark it complete. Pet has a name, a species, and a list of tasks, and you can add tasks to a pet. Owner has a name and a list of pets, and can add pets and pull together all tasks from every pet. Scheduler works with an owner. It will list tasks for today and sort them by time once the logic is written.

b. Design changes

I ended up adding a due date on each task and a pet name on each task so the scheduler can tell what is due today and filter by pet without guessing. I also added real methods on the scheduler for filtering, conflicts, and rolling daily or weekly tasks forward when you mark one done. Later I added priority and duration, JSON save and load on the owner, and extra scheduler helpers. That is more than the first skeleton but it still matches the same four classes, just with more detail filled in.

2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

The scheduler now sorts by priority first and then clock time for today’s open tasks. It still uses a due date so “today” only pulls tasks that are actually due today and not finished yet. Filtering can narrow by whether something is done or which pet it belongs to. If two tasks clash at the same start time you still get a warning instead of the app silently picking one.

b. Tradeoffs

Conflict checking at the exact same time string is still simpler than full overlap logic, but duration is used for the next open slot helper so there is a second opinion when you ask for a free block. That split is a tradeoff between simple warnings and a heavier scheduling model.

3. AI Collaboration

a. How you used AI

I used Cursor with Claude to help scaffold classes, wire Streamlit session state, and write tests when I got stuck on edge cases. The prompts that worked best were the ones where I pasted the exact file or error and asked for a small change, not a whole rewrite.

b. Judgment and verification

Sometimes the model wanted to add extra features or refactor everything at once. I did not always take that. I kept the model focused on one behavior at a time and I checked it by running the demo script and the tests so I could see if the behavior was really right.

4. Testing and Verification

a. What you tested

I tested marking tasks complete, adding tasks to pets, sorting by time, daily and weekly follow-up tasks, conflict warnings when two tasks share a time, empty lists, filtering by pet, a case with no conflict, priority ordering, JSON save and load, and the next slot helper. Those tests matter because they are the main ways this app can break in real use.

b. Confidence

I feel pretty good, maybe a 4 out of 5. If I had more time I would test bad time formats, duplicate pets with the same name, and edge cases around midnight for the slot finder.

5. Reflection

a. What went well

The part I like most is that the same Owner object stays in Streamlit session state, and now it can hydrate from a JSON file so the app feels less fragile between runs.

b. What you would improve

I would add edit and delete for tasks in the UI, and maybe a darker theme toggle. I would also tighten validation on time strings so bad input fails fast.

c. Key takeaway

The important lesson for me is that I still have to be the one deciding what belongs in scope. The AI can write a lot of code fast, but I have to say what done means and check it.

6. Prompt comparison (optional extension)

I asked one model in Cursor for a compact next-slot algorithm and I compared it mentally to a more verbose version that stepped minute by minute. I kept the minute scan because it was easy to read and fast enough for a small task list. If the course had required two different web models, I would run the same prompt in two tools and compare readability and edge cases the same way.
