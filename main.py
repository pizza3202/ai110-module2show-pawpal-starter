from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Alex", available_time_per_day=60, preferences="prefers morning walks")

# Create two pets
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Mochi", species="Cat", age=5)

# Add tasks out of order (with start_times to demo sorting)
dog.add_task(Task(name="Evening Walk",   category="walk",       duration=20, priority="medium",
                  start_time="18:00", frequency="daily"))
dog.add_task(Task(name="Morning Walk",   category="walk",       duration=20, priority="high",
                  start_time="07:00", frequency="daily"))
dog.add_task(Task(name="Flea Medicine",  category="medication", duration=5,  priority="medium",
                  start_time="09:00", frequency="weekly"))
dog.add_task(Task(name="Breakfast",      category="feed",       duration=10, priority="high",
                  start_time="08:00", frequency="daily"))

cat.add_task(Task(name="Brush Fur",      category="grooming",   duration=15, priority="low"))
cat.add_task(Task(name="Dinner",         category="feed",       duration=10, priority="high",
                  start_time="17:30", frequency="daily"))
# Intentional conflict: same start_time as Evening Walk (18:00)
cat.add_task(Task(name="Playtime",       category="enrichment", duration=10, priority="medium",
                  start_time="18:00"))

# Register pets with owner
owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner=owner)

# ── Demo: sort_by_time ────────────────────────────────────────────────────────
print("\n=== All tasks sorted by start time ===")
all_tasks = owner.get_all_tasks()
for t in scheduler.sort_by_time(all_tasks):
    time_label = t.start_time if t.start_time else "no time"
    print(f"  {time_label}  [{t.priority}] {t.name} ({t.frequency})")

# ── Demo: filter_tasks ────────────────────────────────────────────────────────
print("\n=== Buddy's pending tasks ===")
for t in scheduler.filter_tasks(completed=False, pet_name="Buddy"):
    print(f"  {t.name}")

# ── Demo: recurring task ──────────────────────────────────────────────────────
print("\n=== Marking 'Morning Walk' complete (daily → auto-reschedules) ===")
morning_walk = next(t for t in dog.tasks if t.name == "Morning Walk")
print(f"  Before: is_completed={morning_walk.is_completed}, due_date={morning_walk.due_date}")
morning_walk.mark_complete()
print(f"  After:  is_completed={morning_walk.is_completed}, due_date={morning_walk.due_date}")

# ── Generate daily plan ───────────────────────────────────────────────────────
# ── Demo: detect_conflicts ────────────────────────────────────────────────────
print("\n=== Conflict detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(f"  ⚠️  {c}")
else:
    print("  No conflicts found.")

warnings = scheduler.check_constraints()
if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(f"  - {w}")

plan = scheduler.generate_plan()
plan.display()
