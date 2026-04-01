import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = None

st.divider()

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet Setup")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

if st.button("Create Owner & Pet"):
    pet = Pet(name=pet_name, age=int(pet_age), type=species)
    owner = Owner(name=owner_name, email="", phone="")
    owner.addPet(pet)
    st.session_state.owner = owner
    st.success(f"Created owner '{owner_name}' with pet '{pet_name}' ({species}).")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_time = st.text_input("Scheduled time (e.g. 08:00)", value="08:00")
task_freq = st.selectbox("Frequency", ["daily", "weekly", "once"])

if st.button("Add task"):
    if st.session_state.owner is None:
        st.warning("Please create an owner and pet first.")
    else:
        task = Task(
            name=task_title,
            description="",
            time=task_time,
            frequency=task_freq,
            priority=priority,
            duration=int(duration),
        )
        st.session_state.owner.getPets()[0].addTask(task)
        st.success(f"Added task '{task_title}' to {st.session_state.owner.getPets()[0].getName()}.")

# Show current tasks
if st.session_state.owner:
    all_tasks = st.session_state.owner.getAllTasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([{
            "Task": t.getName(),
            "Time": t.getTime(),
            "Duration (min)": t.getDuration(),
            "Priority": t.getPriority(),
            "Frequency": t.getFrequency(),
            "Done": t.isCompleted(),
        } for t in all_tasks])
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Create an owner and pet to get started.")

st.divider()

# --- Schedule & Smart Features ---
st.subheader("Smart Schedule")

sort_mode = st.radio("Sort by", ["Priority", "Time"], horizontal=True)

if st.button("Generate schedule"):
    if st.session_state.owner is None or not st.session_state.owner.getAllTasks():
        st.warning("Add an owner, pet, and at least one task first.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)

        # Conflict detection — shown as warnings before the schedule
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("No scheduling conflicts detected.")

        # Sort by chosen mode
        if sort_mode == "Time":
            scheduled = scheduler.sort_by_time()
            st.info("Showing tasks sorted by scheduled time.")
        else:
            scheduled = scheduler.generateSchedule()
            st.info("Showing tasks sorted by priority (high first).")

        st.table([{
            "Task": t.getName(),
            "Time": t.getTime(),
            "Duration (min)": t.getDuration(),
            "Priority": t.getPriority(),
            "Frequency": t.getFrequency(),
            "Status": "✅ Done" if t.isCompleted() else "⏳ Pending",
        } for t in scheduled])

st.divider()

# --- Filter Tasks ---
st.subheader("Filter Tasks")

filter_status = st.selectbox("Show tasks by status", ["All", "Pending", "Done"])

if st.session_state.owner and st.session_state.owner.getAllTasks():
    scheduler = Scheduler(owner=st.session_state.owner)
    if filter_status == "Pending":
        filtered = scheduler.filter_tasks(completed=False)
    elif filter_status == "Done":
        filtered = scheduler.filter_tasks(completed=True)
    else:
        filtered = scheduler.getAllTasks()

    if filtered:
        st.table([{
            "Task": t.getName(),
            "Time": t.getTime(),
            "Priority": t.getPriority(),
            "Status": "✅ Done" if t.isCompleted() else "⏳ Pending",
        } for t in filtered])
    else:
        st.info(f"No '{filter_status}' tasks found.")
