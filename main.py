# Import classes from pawpal_system.py
import pawpal_system   

# Create an Owner
owner = pawpal_system.Owner(name="Alice", available_minutes=120) 

# Create two Pets
pet1 = pawpal_system.Pet(name="Buddy", species="Dog", breed="Labrador", age=5)
pet2 = pawpal_system.Pet(name="Mittens", species="Cat", breed="Siamese", age=3) 


# Add three tasks with different times to those pets
task1 = pawpal_system.Task(name="Walk", category="walk", duration_minutes=30, daily_frequency=1, priority=1, pet_name="Buddy")
task2 = pawpal_system.Task(name="Feeding", category="feeding", duration_minutes=15, daily_frequency=1, priority=2, pet_name="Buddy")
task3 = pawpal_system.Task(name="Grooming", category="grooming", duration_minutes=45, daily_frequency=1, priority=3, pet_name="Mittens")

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Generate and print the daily schedule
scheduler = pawpal_system.Scheduler(owner)
scheduled_tasks = scheduler.generate_plan()
print(scheduler.explain_plan())
