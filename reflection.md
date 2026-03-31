# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design will have four classes, user, pet, task, and scheduler. The three core actions a user should be able to perform are add a pet, check off tasks for pets, and see their daily task list. For pet class, you should be able to see basic information about the pet like their species and required tasks. You should also be able to add and delete pets. The tasks class allows you to create individual tasks and input information such as for which associated pet, duration of the task, etc. The scheduler class compiles a daily task list for users based on their availability and the duration and priority of different tasks. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my designed changed during actual implementation of the classes. For example, I realized that my original design had no link between Task.pet_name to the actual Pet object. Another problem in my original design was that the .get_daily_plan() method existed in two places, the User and Scheduler class. I used Claude Code, which suggested to remove Owner.get_daily_plan() and just use the Scheduler class to remove duplication and make sure that all scheduling logic was happening under one class only. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One key trade-off is that it optimizes for priority first, not timeline coherence: higher-priority tasks are selected before lower-priority ones, even if that creates an awkward time order (for example, an 08:30 task can be scheduled before a 06:45 task). I think this makes sense for the app because we want to prioritize high priority tasks for different pets so things can be scheduled and completed more efficiently. 



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
