import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Step 2: Session state "memory" ───────────────────────────────────────────
# Streamlit reruns top-to-bottom on every interaction, so we store the Owner
# object in st.session_state so it persists across button clicks.

if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Step 1: Owner + Pet setup ─────────────────────────────────────────────────
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

# ── Add tasks ─────────────────────────────────────────────────────────────────
st.subheader("Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_name = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

category = st.selectbox("Category", ["walk", "feed", "medication", "grooming", "enrichment"])

if st.button("Add Task"):
    if st.session_state.owner is None:
        st.warning("Please save Owner & Pet info first.")
    else:
        task = Task(name=task_name, category=category, duration=int(duration), priority=priority)
        # Add task to the first (and usually only) pet
        st.session_state.owner.pets[0].add_task(task)
        st.success(f"Added task: {task_name}")

# Show current tasks
if st.session_state.owner and st.session_state.owner.get_all_tasks():
    task_data = [
        {"Task": t.name, "Category": t.category, "Duration (min)": t.duration, "Priority": t.priority}
        for t in st.session_state.owner.get_all_tasks()
    ]
    st.write("Current tasks:")
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.warning("Please save Owner & Pet info first.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Please add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)

        warnings = scheduler.check_constraints()
        if warnings:
            for w in warnings:
                st.warning(w)

        plan = scheduler.generate_plan()

        st.success(f"Schedule generated for {plan.date}!")
        st.markdown(f"**Total time:** {plan.total_duration} / {st.session_state.owner.get_available_time()} min")
        st.markdown(f"**Reasoning:** {plan.explanation}")

        st.markdown("### Today's Plan")
        for i, task in enumerate(plan.scheduled_tasks, 1):
            st.markdown(f"{i}. **[{task.priority.upper()}]** {task.name} `{task.category}` — {task.duration} min")
