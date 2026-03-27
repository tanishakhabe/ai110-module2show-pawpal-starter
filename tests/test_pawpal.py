# Task completion
# Verify that calling mark_complete() actually changes the task's status.
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