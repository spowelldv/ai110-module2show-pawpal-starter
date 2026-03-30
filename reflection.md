# PawPal+ Project Reflection

## 1. System Design

A user should be able to add their pets with basic info like name and species so the app knows who needs care. They should be able to schedule care tasks such as walks, feeding, or meds with a time and how often each task repeats. They should also be able to see what is due today in a clear order so nothing important gets skipped.

a. Initial design

The design uses four main classes. Task is one activity. It has a description, a time, how often it happens, and whether it is finished, and there is a way to mark it complete. Pet has a name, a species, and a list of tasks, and you can add tasks to a pet. Owner has a name and a list of pets, and can add pets and pull together all tasks from every pet. Scheduler works with an owner. It will list tasks for today and sort them by time once the logic is written.

b. Design changes

I ended up adding a due date on each task and a pet name on each task so the scheduler can tell what is due today and filter by pet without guessing. I also added real methods on the scheduler for filtering, conflicts, and rolling daily or weekly tasks forward when you mark one done. That is more than the first skeleton but it still matches the same four classes, just with more detail filled in.

---

## 2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

The scheduler mostly cares about the clock time on each task so it can sort in order. It also uses a due date so “today” only pulls tasks that are actually due today and not finished yet. Filtering can narrow by whether something is done or which pet it belongs to. I did not build priority levels yet, so if two things clash the app just warns about the time overlap instead of picking a winner.

b. Tradeoffs

Conflict checking only looks at the exact same time string, not how long a task might run, so two things could still overlap in real life if one is long and the next starts before the first really ends. That is a tradeoff I kept on purpose because it keeps the first version simple and still catches the obvious double booking case when two tasks start at the same minute.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
