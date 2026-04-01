from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    name: str
    description: str
    time: str           # e.g. "08:00"
    frequency: str      # e.g. "daily", "weekly"
    priority: str       # "high", "medium", "low"
    duration: int       # in minutes
    completed: bool = False

    def getName(self) -> str:
        """Return the task name."""
        return self.name

    def getDescription(self) -> str:
        """Return the task description."""
        return self.description

    def getTime(self) -> str:
        """Return the scheduled time for this task."""
        return self.time

    def getFrequency(self) -> str:
        """Return how often the task recurs (e.g. daily, weekly)."""
        return self.frequency

    def getPriority(self) -> str:
        """Return the priority level of the task."""
        return self.priority

    def getDuration(self) -> int:
        """Return the estimated duration in minutes."""
        return self.duration

    def isCompleted(self) -> bool:
        """Return True if the task has been completed."""
        return self.completed

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return a new recurring instance if applicable."""
        self.completed = True
        if self.frequency == "daily":
            next_time = (datetime.strptime(self.time, "%H:%M") + timedelta(days=1)).strftime("%H:%M")
            return Task(self.name, self.description, next_time, self.frequency, self.priority, self.duration)
        elif self.frequency == "weekly":
            next_time = (datetime.strptime(self.time, "%H:%M") + timedelta(weeks=1)).strftime("%H:%M")
            return Task(self.name, self.description, next_time, self.frequency, self.priority, self.duration)
        return None

    def get_summary(self) -> str:
        """Return a formatted one-line summary of the task."""
        status = "Done" if self.completed else "Pending"
        return f"{self.name} at {self.time} ({self.duration} mins, {self.priority} priority) - {status}"


@dataclass
class Pet:
    name: str
    age: int
    type: str
    tasks: List[Task] = field(default_factory=list)

    def getName(self) -> str:
        """Return the pet's name."""
        return self.name

    def getAge(self) -> int:
        """Return the pet's age."""
        return self.age

    def getType(self) -> str:
        """Return the type/species of the pet."""
        return self.type

    def getTasks(self) -> List[Task]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks

    def addTask(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    email: str
    phone: str
    pets: List[Pet] = field(default_factory=list)

    def getName(self) -> str:
        """Return the owner's name."""
        return self.name

    def getEmail(self) -> str:
        """Return the owner's email address."""
        return self.email

    def getPhone(self) -> str:
        """Return the owner's phone number."""
        return self.phone

    def getPets(self) -> List[Pet]:
        """Return the list of pets owned by this owner."""
        return self.pets

    def addPet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def getAllTasks(self) -> List[Task]:
        """Return all tasks across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.getTasks())
        return all_tasks


@dataclass
class Scheduler:
    owner: Owner

    def getAllTasks(self) -> List[Task]:
        """Return all tasks for the owner's pets."""
        return self.owner.getAllTasks()

    def generateSchedule(self) -> List[Task]:
        """Return all tasks sorted by priority (high first)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        all_tasks = self.getAllTasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order.get(t.getPriority(), 3))
        return sorted_tasks

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by their scheduled time (HH:MM)."""
        return sorted(self.getAllTasks(), key=lambda t: t.getTime())

    def filter_tasks(self, pet_name: str = "", completed: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        results = []
        for pet in self.owner.getPets():
            if pet_name and pet.getName().lower() != pet_name.lower():
                continue
            for task in pet.getTasks():
                if completed is not None and task.isCompleted() != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same time."""
        seen = {}
        warnings = []
        for task in self.getAllTasks():
            if task.getTime() in seen:
                warnings.append(
                    f"Conflict at {task.getTime()}: '{seen[task.getTime()]}' and '{task.getName()}'"
                )
            else:
                seen[task.getTime()] = task.getName()
        return warnings

    def printSchedule(self) -> None:
        """Print the prioritized daily schedule to the console."""
        print(f"\nToday's Schedule for {self.owner.getName()}'s pets:")
        print("-" * 40)
        tasks = self.generateSchedule()
        if not tasks:
            print("No tasks scheduled.")
        for task in tasks:
            print(task.get_summary())
