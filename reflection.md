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

The initial design had five classes: **Owner** (holds user info and daily time budget), **Pet** (stores pet profile), **Task** (represents one care activity with duration and priority), **Scheduler** (takes owner/pet/tasks and produces a plan), and **DailyPlan** (stores and displays the final schedule with reasoning). Relationships: Owner owns a Pet, Scheduler reads from all three and outputs a DailyPlan.

**b. Design changes**

Yes. After reviewing the skeleton, I moved the task list into `Pet` (adding `tasks`, `add_task()`, and `remove_task()` to the `Pet` class). Originally, `Scheduler` held the task list directly, which created ambiguity about who owned the tasks. Since tasks belong to a pet's care routine, it makes more sense for `Pet` to be the source of truth, and for `Scheduler` to read from `pet.tasks`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: the owner's **daily time budget** (total minutes available) and each task's **priority level** (high, medium, low). Tasks are sorted by priority first, then by shortest duration, and the scheduler greedily fits as many as possible within the time budget — skipping any that would exceed it.

Time budget was the most important constraint because it directly limits what is physically possible in a day. Priority was second because it ensures critical care (medications, feeding) always gets scheduled before optional activities (grooming, enrichment).

**b. Tradeoffs**

The conflict detector only flags tasks that share the **exact same `start_time` string** (e.g. both set to `"18:00"`). It does not check whether task durations cause overlap — for example, a 30-minute task at `"17:45"` and a task at `"18:00"` would not be flagged even though they overlap in real time.

This tradeoff is reasonable for a first version because most pet care tasks are short and loosely scheduled. Requiring exact duration-overlap math would add significant complexity (converting times to minutes, checking ranges) for little practical gain at this scale. A future improvement would be to track actual end times and detect range overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used throughout every phase: brainstorming the initial class structure and UML diagram, generating Python class skeletons from the UML, implementing scheduling logic (priority sorting, greedy plan generation, recurring tasks, conflict detection), writing the test suite, and wiring the backend to the Streamlit UI.

The most effective prompts were specific and structural — for example, asking for a Mermaid class diagram based on named attributes and methods, or asking to implement a specific method (like `detect_conflicts`) with a clear description of its expected behavior. Vague prompts produced generic code; specific prompts produced code that fit the existing design.

**b. Judgment and verification**

When AI first generated the `Scheduler` class, it held the task list directly as `self.tasks`. I rejected this because it created ambiguity — tasks logically belong to a pet, not the scheduler. I moved the task list into `Pet` and had `Scheduler` read from `owner.get_all_tasks()` instead. I verified this by tracing the data flow: the owner owns pets, pets own tasks, and the scheduler only reads and organizes — it does not store data. This matched the single-responsibility principle more cleanly.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers 12 behaviors across five areas: task completion (`mark_complete()` sets the flag), task addition (pet task count increases), sorting correctness (tasks returned in chronological HH:MM order, untimed tasks last), recurrence logic (daily tasks reschedule to tomorrow, weekly to next week, once tasks stay completed), conflict detection (duplicate start times flagged, unique times and no-time tasks pass cleanly), and edge cases (empty task list returns an empty plan, tasks exceeding the time budget are skipped).

These tests were important because the scheduler's core value — fitting the right tasks into a limited day — depends entirely on correct prioritization and constraint checking. A bug in `generate_plan` or `mark_complete` would silently produce wrong schedules.

**b. Confidence**

Confidence level: ★★★★☆. The core scheduling behaviors (priority ordering, time budget, recurrence, conflict detection) are all tested and passing. Less confident about multi-pet edge cases, tasks with identical names across different pets, and preference-based ordering, which are not yet tested. UI integration (e.g. what happens if the user generates a schedule twice in a row) is also untested.

---

## 5. Reflection

**a. What went well**

The separation between the logic layer (`pawpal_system.py`) and the UI (`app.py`) worked well. Because all scheduling logic lived in Python classes, it was easy to test independently and then connect to Streamlit without rewriting anything. The greedy scheduling algorithm was also simple to reason about and debug — the explanation text made it easy to verify the output was correct.

**b. What you would improve**

I would add duration-overlap conflict detection instead of exact start-time matching. The current detector misses cases where a 30-minute task at 17:45 overlaps with a task at 18:00. I would also add support for multiple pets with separate schedules displayed side by side, and allow the user to mark tasks complete directly in the UI rather than only in code.

**c. Key takeaway**

The most important lesson was that AI is a fast and capable collaborator, but it needs the human to act as the architect. AI will generate working code quickly, but without a clear design (UML, class responsibilities, data ownership), the generated code drifts toward whatever is easiest rather than what is correct for the system. Deciding that `Pet` owns tasks, not `Scheduler`, was a human judgment call that made the entire system cleaner — AI would not have made that call on its own without being guided.
