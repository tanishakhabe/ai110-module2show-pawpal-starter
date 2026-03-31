# Task completion
# Verify that calling mark_complete() actually changes the task's status.
from datetime import timedelta

import pawpal_system


def test_task_completion():
    task = pawpal_system.Task(name="Test Task", category="test", duration_minutes=10, daily_frequency=1, priority=1, pet_name="Test Pet")
    assert not task.completed, "Task should initially be incomplete."
    task.mark_complete()
    assert task.completed, "Task should be marked as complete after calling mark_complete()."
    

# Task addition
# Verify that adding a task to a Pet increases that pet's task count
def test_task_addition():
    pet = pawpal_system.Pet(name="Test Pet", species="Test Species", breed="Test Breed", age=1)
    initial_task_count = len(pet.tasks)
    task = pawpal_system.Task(name="Test Task", category="test", duration_minutes=10, daily_frequency=1, priority=1, pet_name="Test Pet")
    pet.add_task(task)
    assert len(pet.tasks) == initial_task_count + 1, "Adding a task should increase the pet's task count by 1."


def test_daily_recurrence_creates_next_task():
    owner = pawpal_system.Owner(name="Test Owner", available_minutes=60)
    pet = pawpal_system.Pet(name="Test Pet", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)

    task = pawpal_system.Task(
        name="Daily Walk",
        category="walk",
        duration_minutes=20,
        daily_frequency=1,
        priority=1,
        pet_name="Test Pet",
        recurrence="daily",
    )
    pet.add_task(task)

    scheduler = pawpal_system.Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)

    assert task.completed, "Original task should be marked complete."
    assert next_task is not None, "A new task should be created for recurring tasks."
    assert next_task.due_date == task.due_date + timedelta(days=1), "Daily recurrence should move due date by one day."
    assert next_task in pet.tasks, "Next recurring task should be added to pet task list."


def test_detect_time_conflicts_for_same_and_different_pets():
    owner = pawpal_system.Owner(name="Test Owner", available_minutes=120)
    buddy = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=4)
    mittens = pawpal_system.Pet(name="Mittens", species="Cat", breed="Mixed", age=2)
    owner.add_pet(buddy)
    owner.add_pet(mittens)

    # Two tasks for Buddy at the same time (same-pet conflict).
    buddy.add_task(
        pawpal_system.Task(
            name="Buddy Walk",
            category="walk",
            duration_minutes=20,
            daily_frequency=1,
            priority=1,
            pet_name="Buddy",
            time="08:00",
        )
    )
    buddy.add_task(
        pawpal_system.Task(
            name="Buddy Breakfast",
            category="feeding",
            duration_minutes=10,
            daily_frequency=1,
            priority=2,
            pet_name="Buddy",
            time="08:00",
        )
    )

    # One task for Mittens at the same time (different-pet conflict with Buddy tasks).
    mittens.add_task(
        pawpal_system.Task(
            name="Mittens Medication",
            category="meds",
            duration_minutes=5,
            daily_frequency=1,
            priority=1,
            pet_name="Mittens",
            time="08:00",
        )
    )

    scheduler = pawpal_system.Scheduler(owner)
    conflicts = scheduler.detect_time_conflicts()

    assert len(conflicts) == 3, "Three tasks at the same time should yield three conflicting pairs."
    assert any(a.pet_name == b.pet_name for a, b in conflicts), "Should detect conflicts for tasks from the same pet."
    assert any(a.pet_name != b.pet_name for a, b in conflicts), "Should detect conflicts for tasks from different pets."


def test_conflict_warnings_are_non_fatal():
    owner = pawpal_system.Owner(name="Owner", available_minutes=120)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=3)
    owner.add_pet(pet)

    pet.add_task(
        pawpal_system.Task(
            name="Walk",
            category="walk",
            duration_minutes=20,
            daily_frequency=1,
            priority=1,
            pet_name="Buddy",
            time="08:00",
        )
    )
    pet.add_task(
        pawpal_system.Task(
            name="Breakfast",
            category="feeding",
            duration_minutes=10,
            daily_frequency=1,
            priority=2,
            pet_name="Buddy",
            time="08:00",
        )
    )

    scheduler = pawpal_system.Scheduler(owner)
    plan, warnings = scheduler.generate_plan_with_warnings()

    assert len(plan) == 2, "Plan should still be generated even when conflicts exist."
    assert warnings, "Conflicts should produce warning messages."
    assert warnings[0].startswith("Warning:"), "Warnings should be clearly labeled."