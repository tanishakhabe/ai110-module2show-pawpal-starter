from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    category: str          # e.g. "walk", "feeding", "meds", "grooming"
    duration_minutes: int
    daily_frequency: int
    priority: int          # 1 = highest priority
    pet_name: str          # name of the associated pet
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize a scheduler for a specific owner."""
        self.owner = owner
        self.scheduled_tasks: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """Build a time-limited schedule ordered by task priority."""
        self.scheduled_tasks = []
        time_used = 0
        for task in self.filter_by_priority():
            if self.fits_in_time(task, time_used):
                self.scheduled_tasks.append(task)
                time_used += task.duration_minutes
        return self.scheduled_tasks

    def filter_by_priority(self) -> list[Task]:
        """Return all pet tasks sorted by ascending priority value."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return sorted(all_tasks, key=lambda t: t.priority)

    def fits_in_time(self, task: Task, time_used: int) -> bool:
        """Check whether adding a task stays within available time."""
        return time_used + task.duration_minutes <= self.owner.available_minutes

    def explain_plan(self) -> str:
        """Return a readable summary of the generated schedule."""
        if not self.scheduled_tasks:
            return "No plan generated yet. Call generate_plan() first."
        lines = [f"Plan for {self.owner.name} ({self.owner.available_minutes} min available):\n"]
        time_used = 0
        for task in self.scheduled_tasks:
            lines.append(
                f"- [{task.priority}] {task.pet_name}: {task.name} ({task.duration_minutes} min)"
            )
            time_used += task.duration_minutes
        lines.append(f"\nTotal time scheduled: {time_used} min")
        return "\n".join(lines)
