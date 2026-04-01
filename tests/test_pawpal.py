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


def test_exact_time_budget_boundary_includes_last_task():
    owner = pawpal_system.Owner(name="Boundary Owner", available_minutes=30)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=4)
    owner.add_pet(pet)

    pet.add_task(
        pawpal_system.Task(
            name="Task A",
            category="care",
            duration_minutes=10,
            daily_frequency=1,
            priority=1,
            pet_name="Buddy",
            time="08:00",
        )
    )
    pet.add_task(
        pawpal_system.Task(
            name="Task B",
            category="care",
            duration_minutes=20,
            daily_frequency=1,
            priority=2,
            pet_name="Buddy",
            time="09:00",
        )
    )

    scheduler = pawpal_system.Scheduler(owner)
    plan = scheduler.generate_plan()

    assert len(plan) == 2, "Both tasks should be included when total duration exactly matches available time."
    assert sum(task.duration_minutes for task in plan) == 30


def test_just_over_budget_rejects_extra_task():
    owner = pawpal_system.Owner(name="Budget Owner", available_minutes=30)
    pet = pawpal_system.Pet(name="Mittens", species="Cat", breed="Mixed", age=2)
    owner.add_pet(pet)

    pet.add_task(
        pawpal_system.Task(
            name="Task A",
            category="care",
            duration_minutes=10,
            daily_frequency=1,
            priority=1,
            pet_name="Mittens",
            time="08:00",
        )
    )
    pet.add_task(
        pawpal_system.Task(
            name="Task B",
            category="care",
            duration_minutes=20,
            daily_frequency=1,
            priority=2,
            pet_name="Mittens",
            time="09:00",
        )
    )
    pet.add_task(
        pawpal_system.Task(
            name="Task C",
            category="care",
            duration_minutes=1,
            daily_frequency=1,
            priority=3,
            pet_name="Mittens",
            time="10:00",
        )
    )

    scheduler = pawpal_system.Scheduler(owner)
    plan = scheduler.generate_plan()

    assert len(plan) == 2, "The task that pushes usage 1 minute over budget should be excluded."
    assert all(task.name != "Task C" for task in plan)


def test_priority_time_mismatch_is_predictable():
    owner = pawpal_system.Owner(name="Priority Owner", available_minutes=60)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=5)
    owner.add_pet(pet)

    pet.add_task(
        pawpal_system.Task(
            name="Earlier Low Priority",
            category="care",
            duration_minutes=10,
            daily_frequency=1,
            priority=3,
            pet_name="Buddy",
            time="06:30",
        )
    )
    pet.add_task(
        pawpal_system.Task(
            name="Later High Priority",
            category="care",
            duration_minutes=10,
            daily_frequency=1,
            priority=1,
            pet_name="Buddy",
            time="08:30",
        )
    )

    scheduler = pawpal_system.Scheduler(owner)
    plan = scheduler.generate_plan()

    assert plan[0].name == "Later High Priority"
    assert plan[1].name == "Earlier Low Priority"


def test_stable_ordering_on_tie_priority_uses_insertion_order():
    owner = pawpal_system.Owner(name="Tie Owner", available_minutes=60)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=5)
    owner.add_pet(pet)

    first = pawpal_system.Task(
        name="First Inserted",
        category="care",
        duration_minutes=10,
        daily_frequency=1,
        priority=2,
        pet_name="Buddy",
        time="09:00",
    )
    second = pawpal_system.Task(
        name="Second Inserted",
        category="care",
        duration_minutes=10,
        daily_frequency=1,
        priority=2,
        pet_name="Buddy",
        time="08:00",
    )
    pet.add_task(first)
    pet.add_task(second)

    scheduler = pawpal_system.Scheduler(owner)
    by_priority = scheduler.filter_by_priority()

    assert by_priority[0].name == "First Inserted"
    assert by_priority[1].name == "Second Inserted"


def test_sorting_correctness_returns_chronological_order():
    owner = pawpal_system.Owner(name="Sort Owner", available_minutes=60)
    scheduler = pawpal_system.Scheduler(owner)
    tasks = [
        pawpal_system.Task("B", "care", 10, 1, 1, "Buddy", time="12:00"),
        pawpal_system.Task("C", "care", 10, 1, 1, "Buddy", time="18:30"),
        pawpal_system.Task("A", "care", 10, 1, 1, "Buddy", time="06:15"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["06:15", "12:00", "18:30"]


def test_hhmm_parsing_edge_cases_are_consistent():
    owner = pawpal_system.Owner(name="Time Owner", available_minutes=60)
    scheduler = pawpal_system.Scheduler(owner)
    tasks = [
        pawpal_system.Task("T1", "care", 5, 1, 1, "Buddy", time="23:59"),
        pawpal_system.Task("T2", "care", 5, 1, 1, "Buddy", time="00:00"),
        pawpal_system.Task("T3", "care", 5, 1, 1, "Buddy", time="9:5"),
        pawpal_system.Task("T4", "care", 5, 1, 1, "Buddy", time="24:00"),
        pawpal_system.Task("T5", "care", 5, 1, 1, "Buddy", time="9:75"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["00:00", "9:5", "9:75", "23:59", "24:00"]


def test_recurrence_logic_daily_completion_creates_next_day_task():
    owner = pawpal_system.Owner(name="Recurrence Owner", available_minutes=60)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)
    task = pawpal_system.Task(
        name="Daily Walk",
        category="walk",
        duration_minutes=20,
        daily_frequency=1,
        priority=1,
        pet_name="Buddy",
        recurrence="daily",
    )
    pet.add_task(task)

    scheduler = pawpal_system.Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)

    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(days=1)


def test_conflict_detection_flags_duplicate_times():
    owner = pawpal_system.Owner(name="Conflict Owner", available_minutes=60)
    pet = pawpal_system.Pet(name="Buddy", species="Dog", breed="Mixed", age=2)
    owner.add_pet(pet)
    pet.add_task(pawpal_system.Task("Walk", "care", 10, 1, 1, "Buddy", time="08:00"))
    pet.add_task(pawpal_system.Task("Breakfast", "care", 10, 1, 2, "Buddy", time="08:00"))

    scheduler = pawpal_system.Scheduler(owner)
    conflicts = scheduler.detect_time_conflicts()

    assert len(conflicts) == 1