# PawPal+ Project Reflection

## 1. System Design

A user should be able to add their pets with basic info like name and species so the app knows who needs care. They should be able to schedule care tasks such as walks, feeding, or meds with a time and how often each task repeats. They should also be able to see what is due today in a clear order so nothing important gets skipped.

a. Initial design

The design uses four main classes. Task is one activity. It has a description, a time, how often it happens, and whether it is finished, and there is a way to mark it complete. Pet has a name, a species, and a list of tasks, and you can add tasks to a pet. Owner has a name and a list of pets, and can add pets and pull together all tasks from every pet. Scheduler works with an owner. It will list tasks for today and sort them by time once the logic is written.

b. Design changes

Nothing has changed yet. The starter code in pawpal_system.py still matches this first design. If I change something later during coding or testing I will write it down here.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
