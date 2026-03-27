# Generating skeletons of the classes (the names, attributes, and empty method stubs) based on the UML.

from dataclasses import dataclass, field

@dataclass
class Task:
    name: str
    category: str          # e.g. "walk", "feeding", "meds", "grooming"
    duration_minutes: int
    priority: int          # 1 = highest priority
    pet_name: Pet          # name of the associated pet
    completed: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_pending_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    email: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: list[Task] = []

    def generate_plan(self) -> list[Task]:
        pass

    def filter_by_priority(self) -> list[Task]:
        pass

    def fits_in_time(self, task: Task, time_used: int) -> bool:
        pass

    def explain_plan(self) -> str:
        pass
