from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations


@dataclass
class Task:
    name: str
    category: str          # e.g. "walk", "feeding", "meds", "grooming"
    duration_minutes: int
    daily_frequency: int
    priority: int          # 1 = highest priority
    pet_name: str          # name of the associated pet
    time: str = "00:00"   # start time in HH:MM format
    recurrence: str = "once"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
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

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by HH:MM time using numeric (hour, minute) comparison."""
        return sorted(tasks, key=lambda t: tuple(map(int, t.time.split(":"))))

    def detect_time_conflicts(self, tasks: list[Task] | None = None) -> list[tuple[Task, Task]]:
        """Find all pairwise conflicts where two tasks share the same start time."""
        if tasks is None:
            if self.scheduled_tasks:
                tasks = self.scheduled_tasks
            else:
                tasks = []
                for pet in self.owner.pets:
                    tasks.extend(pet.tasks)

        grouped_by_time: dict[str, list[Task]] = {}
        for task in tasks:
            grouped_by_time.setdefault(task.time, []).append(task)

        conflicts: list[tuple[Task, Task]] = []
        for same_time_tasks in grouped_by_time.values():
            if len(same_time_tasks) > 1:
                conflicts.extend(combinations(same_time_tasks, 2))

        return conflicts

    def get_conflict_warnings(self, tasks: list[Task] | None = None) -> list[str]:
        """Convert detected time conflicts into non-fatal warning messages."""
        warnings: list[str] = []
        for task_a, task_b in self.detect_time_conflicts(tasks):
            warnings.append(
                f"Warning: '{task_a.name}' ({task_a.pet_name}) conflicts with "
                f"'{task_b.name}' ({task_b.pet_name}) at {task_a.time}."
            )
        return warnings

    def generate_plan_with_warnings(self) -> tuple[list[Task], list[str]]:
        """Generate a schedule and return it alongside any conflict warnings."""
        plan = self.generate_plan()
        return plan, self.get_conflict_warnings(plan)

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and, for daily/weekly recurrence, create its next occurrence."""
        task.mark_complete()

        recurrence = task.recurrence.lower()
        if recurrence == "daily":
            next_due_date = task.due_date + timedelta(days=1)
        elif recurrence == "weekly":
            next_due_date = task.due_date + timedelta(days=7)
        else:
            return None

        next_task = Task(
            name=task.name,
            category=task.category,
            duration_minutes=task.duration_minutes,
            daily_frequency=task.daily_frequency,
            priority=task.priority,
            pet_name=task.pet_name,
            time=task.time,
            recurrence=task.recurrence,
            due_date=next_due_date,
            completed=False,
        )

        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                return next_task

        return next_task

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
                f"- [{task.priority}] {task.time} {task.pet_name}: {task.name} ({task.duration_minutes} min)"
            )
            time_used += task.duration_minutes
        lines.append(f"\nTotal time scheduled: {time_used} min")
        return "\n".join(lines)
