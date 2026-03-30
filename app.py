import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your smart daily pet care planner.")

if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner & Pet setup ──────────────────────────────────────────────────────────
st.subheader("Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=60)
    preferences = st.text_input("Preferences (optional)", value="prefers morning walks")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
    age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, age=int(age))
    owner = Owner(name=owner_name, available_time_per_day=int(available_time), preferences=preferences)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Saved! {owner_name} owns {pet_name} the {species}.")

st.divider()

# ── Add tasks ──────────────────────────────────────────────────────────────────
st.subheader("Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_name = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5, col6 = st.columns(3)
with col4:
    category = st.selectbox("Category", ["walk", "feed", "medication", "grooming", "enrichment"])
with col5:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
with col6:
    start_time = st.text_input("Start time (HH:MM, optional)", value="")

if st.button("Add Task"):
    if st.session_state.owner is None:
        st.warning("Please save Owner & Pet info first.")
    else:
        task = Task(
            name=task_name,
            category=category,
            duration=int(duration),
            priority=priority,
            frequency=frequency,
            start_time=start_time.strip() or None,
        )
        st.session_state.owner.pets[0].add_task(task)
        st.success(f"Added: {task_name} ({frequency})")

# Show current tasks sorted by time
if st.session_state.owner and st.session_state.owner.get_all_tasks():
    scheduler = Scheduler(owner=st.session_state.owner)
    sorted_tasks = scheduler.sort_by_time(st.session_state.owner.get_all_tasks())

    task_data = [
        {
            "Task": t.name,
            "Category": t.category,
            "Duration (min)": t.duration,
            "Priority": t.priority,
            "Frequency": t.frequency,
            "Start Time": t.start_time or "—",
        }
        for t in sorted_tasks
    ]
    st.write("Current tasks (sorted by start time):")
    st.table(task_data)

    # Show conflict warnings inline
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.error("**Scheduling conflicts detected:**")
        for c in conflicts:
            st.warning(f"⚠️ {c}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate schedule ──────────────────────────────────────────────────────────
st.subheader("Generate Today's Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.warning("Please save Owner & Pet info first.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Please add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)

        # Conflict warnings
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("Fix these conflicts before relying on this schedule:")
            for c in conflicts:
                st.warning(f"⚠️ {c}")

        # Time budget warnings
        for w in scheduler.check_constraints():
            st.warning(w)

        plan = scheduler.generate_plan()

        st.success(f"Schedule generated for {plan.date}")
        st.markdown(f"**Time used:** {plan.total_duration} / {st.session_state.owner.get_available_time()} min")

        st.markdown("### Today's Plan")
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        for i, task in enumerate(plan.scheduled_tasks, 1):
            icon = priority_icon.get(task.priority, "⚪")
            time_label = f" @ {task.start_time}" if task.start_time else ""
            st.markdown(f"{i}. {icon} **{task.name}** `{task.category}`{time_label} — {task.duration} min · _{task.frequency}_")

        with st.expander("Reasoning"):
            st.write(plan.explanation)
