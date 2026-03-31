import streamlit as st
import pawpal_system

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=600, value=60)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = pawpal_system.Owner(name=owner_name, available_minutes=int(available_minutes))

owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes = int(available_minutes)


def get_or_create_pet(owner_obj: pawpal_system.Owner, name: str, species_name: str) -> pawpal_system.Pet:
    """Return an existing pet by name or create and add it to the owner."""
    for existing_pet in owner_obj.pets:
        if existing_pet.name == name:
            return existing_pet

    new_pet = pawpal_system.Pet(name=name, species=species_name, breed="Unknown", age=1)
    owner_obj.add_pet(new_pet)
    return new_pet

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_map = {"high": 1, "medium": 2, "low": 3}
    pet = get_or_create_pet(owner, pet_name, species)
    task = pawpal_system.Task(
        name=task_title,
        category="general",
        duration_minutes=int(duration),
        daily_frequency=1,
        priority=priority_map[priority],
        pet_name=pet.name,
    )
    pet.add_task(task)

    st.session_state.tasks = [
        {
            "pet": t.pet_name,
            "title": t.name,
            "duration_minutes": t.duration_minutes,
            "priority": t.priority,
            "completed": t.completed,
        }
        for p in owner.pets
        for t in p.tasks
    ]

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using your backend scheduling logic.")

if st.button("Generate schedule"):
    scheduler = pawpal_system.Scheduler(owner)
    scheduled_tasks = scheduler.generate_plan()

    if scheduled_tasks:
        st.success("Schedule generated.")
        st.text(scheduler.explain_plan())
    else:
        st.info("No tasks fit into the current time window. Add tasks or increase available minutes.")
