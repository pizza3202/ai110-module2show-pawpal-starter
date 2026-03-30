# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:

1. **Enter owner and pet info** — The user provides basic details about themselves and their pet (name, pet type, available time per day, and any preferences or constraints).
2. **Add and edit care tasks** — The user can create, update, or remove pet care tasks such as walks, feeding, medications, grooming, or enrichment activities. Each task has at minimum a duration and a priority level.
3. **Generate a daily schedule/plan** — The user triggers the scheduler to produce a daily care plan based on the tasks and constraints entered. The app displays the plan and explains why it was arranged that way.

Main building blocks (objects) for PawPal+:

**Owner**
- Attributes: `name`, `available_time_per_day` (minutes), `preferences` (e.g. prefers morning walks)
- Methods: `get_available_time()`, `update_preferences()`

**Pet**
- Attributes: `name`, `species`, `age`, `owner`
- Methods: `get_info()`

**Task**
- Attributes: `name`, `category` (walk/feed/medication/grooming/enrichment), `duration` (minutes), `priority` (high/medium/low), `is_completed`
- Methods: `mark_complete()`, `update()`

**Scheduler**
- Attributes: `tasks`, `owner`, `pet`
- Methods: `generate_plan()`, `prioritize_tasks()`, `check_constraints()`

**DailyPlan**
- Attributes: `date`, `scheduled_tasks`, `total_duration`, `explanation`
- Methods: `display()`, `get_summary()`

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
