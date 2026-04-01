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

My scheduler primarily considers the user's available time blocks, the duration and priority of each task, and some basic pet-related preferences such as frequency (daily vs. weekly tasks) and time-of-day constraints, because some tasks can only be completed at specific times of the day.

I treated time and task priority as the most important constraints, because the scheduler must first ensure that tasks physically fit into the user's day and that urgent or high-importance tasks for the pet are scheduled before more flexible ones. I wanted to make sure that hte generated schedule is realistic and ensures critical care tasks are not missed.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One key trade-off is that it optimizes for priority first, not timeline coherence. SO higher-priority tasks are selected before lower-priority ones, even if that creates an awkward time order (for example, an 08:30 task can be scheduled before a 06:45 task). I think this makes sense for the app because we want to prioritize high priority tasks for different pets so things can be scheduled and completed more efficiently. 



---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I mostly used Copilot Chat Plan mode and Agent mode. I feel like the agent mode was really good with coming up with very a wide variety of test cases and designing them and checking if they pass. I also used the Plan mode to figure out in what steps to start building the additional features. Using Copilot Plan mode made the building process a little less overwhelming because it provided a nice structure. After building each feature, I immediately tried the test cases which also made debugging easier. 

I asked Copilot why it chose to include certain functions and what were the trade offs. I also chose to provide specific files as context to the Chat when I was prompting. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I was trying to improve the scheduling feature, one of the AI suggestions was building separate daily and weekly schedules and allowing rescheduling. I thought that would be a bit complicated for a first version of my app and didn't feel like I understood the exact changes it was suggesting. So I evaluated and decided not to accepted the other features. 

There were other times when I didn't fully understand the AI outputted code, so I would also use the Copilot Chat to ask it to explain the output and try to manually walk through the code. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested core scheduling and reliability behaviors: exact time-budget boundaries, just-over-budget exclusion, priority-based selection, tie-priority ordering consistency, time sorting correctness, HH:MM edge-case ordering, daily recurrence creation, and conflict detection/warning behavior for duplicate times. I also tested task completion and task addition basics to confirm the core object interactions were stable before testing the added scheduling class logic.

These tests verify that the scheduler behaves correctly in realistic, every day edge cases that could occur in the app, especially around time limits, ordering, and recurring updates to the daily schedule. They were important because users need predictable scheduling decisions and safe handling of conflicts and recurrence without the app crashing.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am pretty confident that my scheduler works correctly. I think some edge cases that I could test next time would be adding in weird inputs (blank inputs, out of range times, etc.) to see if the app still handles weird user inputs safely without crashing, since in those cases it would be better to deploy messages or warnings.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I liked the ease of building with Copilot because it really streamlined the process. I basically decided how I wanted to build the features using Plan mode, and then had the Agent mode do most of the actual fine-grain coding. I also immediately tested each feature so everything kind of stacked on top of each other seamlessly. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would definitely want to improve the UI since there are a lot of places where it feels unnecessarily clunky and could lead to errors. With task title, I would also like to add a task category option so owners could schedule similar tasks around the same time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned about designing systems is the importance of building a lot of small tests and checking for edge cases in your tests. Especially when you are working with an app that has a lot of different components. I also tried to walk through the user journey and think about the app development process through the user's lens. This also helped me when writing the prompts for Copilot, by specifying to focus on a streamlined user journey.