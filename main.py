# Import classes from pawpal_system.py
import pawpal_system   

# Create an Owner
owner = pawpal_system.Owner(name="Alice", available_minutes=120) 

# Create two Pets
pet1 = pawpal_system.Pet(name="Buddy", species="Dog", breed="Labrador", age=5)
pet2 = pawpal_system.Pet(name="Mittens", species="Cat", breed="Siamese", age=3) 


# Add tasks out of order (by both priority and time)
pet1.add_task(
    pawpal_system.Task(
        name="Feeding",
        category="feeding",
        duration_minutes=15,
        daily_frequency=1,
        priority=3,
        pet_name="Buddy",
        time="07:15",
        recurrence="daily",
    )
)
pet1.add_task(
    pawpal_system.Task(
        name="Walk",
        category="walk",
        duration_minutes=30,
        daily_frequency=1,
        priority=1,
        pet_name="Buddy",
        time="08:30",
        recurrence="once",
    )
)
pet2.add_task(
    pawpal_system.Task(
        name="Medication",
        category="meds",
        duration_minutes=10,
        daily_frequency=1,
        priority=2,
        pet_name="Mittens",
        time="06:45",
        recurrence="weekly",
    )
)
pet2.add_task(
    pawpal_system.Task(
        name="Grooming",
        category="grooming",
        duration_minutes=45,
        daily_frequency=1,
        priority=4,
        pet_name="Mittens",
        time="09:00",
        recurrence="once",
    )
)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Build scheduler
scheduler = pawpal_system.Scheduler(owner)

# Show original insertion order
all_tasks = [task for pet in owner.pets for task in pet.tasks]
print("Original task order (insertion order):")
for task in all_tasks:
    print(f"P{task.priority} | {task.time} | {task.name} ({task.pet_name})")

# Use filtering method: sorted by priority
priority_sorted_tasks = scheduler.filter_by_priority()
print("\nFiltered by priority (Scheduler.filter_by_priority):")
for task in priority_sorted_tasks:
    print(f"P{task.priority} | {task.time} | {task.name} ({task.pet_name})")

# Use sorting method: sorted by time
time_sorted_tasks = scheduler.sort_by_time(all_tasks)
print("\nSorted by time (Scheduler.sort_by_time):")
for task in time_sorted_tasks:
    print(f"P{task.priority} | {task.time} | {task.name} ({task.pet_name})")

# Generate and print a schedule (priority-first, with time limit)
scheduled_tasks = scheduler.generate_plan()
print("\nGenerated plan:")
print(scheduler.explain_plan())

# Demonstrate recurrence rollover using timedelta in Scheduler.mark_task_complete
daily_task = pet1.tasks[0]
weekly_task = pet2.tasks[0]

next_daily = scheduler.mark_task_complete(daily_task)
next_weekly = scheduler.mark_task_complete(weekly_task)

print("\nRecurrence rollover check:")
if next_daily:
    print(
        f"Daily task '{daily_task.name}' completed on {daily_task.due_date} -> next due {next_daily.due_date}"
    )
if next_weekly:
    print(
        f"Weekly task '{weekly_task.name}' completed on {weekly_task.due_date} -> next due {next_weekly.due_date}"
    )
