from pawpal_system import Owner, Pet, Task, Scheduler

owner1 = Owner("Rashmi", "rashmi@gmail.com", "12-456")

pet1 = Pet("Buddy", 3, "dog")
pet2 = Pet("Luna", 2, "cat")

# Tasks added out of order to test sorting
pet1.addTask(Task("Morning Walk", "Walk around the block", "08:00", "daily", "high", 30))
pet1.addTask(Task("Evening Feed", "Dry kibble", "18:00", "daily", "medium", 10))
pet2.addTask(Task("Feeding", "Feed Almond Milk", "10:00", "daily", "high", 10))
pet2.addTask(Task("Playtime", "Interactive toys", "08:00", "weekly", "low", 20))  # conflict with Buddy's walk

owner1.addPet(pet1)
owner1.addPet(pet2)

scheduler = Scheduler(owner1)

# --- Priority schedule ---
print("=== Priority Schedule ===")
scheduler.printSchedule()

# --- Sort by time ---
print("\n=== Sorted by Time ===")
for task in scheduler.sort_by_time():
    print(task.get_summary())

# --- Filter by pet ---
print("\n=== Filter: Buddy's tasks only ===")
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(task.get_summary())

# --- Filter by completion status ---
print("\n=== Filter: Pending tasks only ===")
for task in scheduler.filter_tasks(completed=False):
    print(task.get_summary())

# --- Recurring task demo ---
print("\n=== Recurring Task Demo ===")
walk = pet1.getTasks()[0]
print(f"Completing: {walk.getName()}")
next_task = walk.mark_complete()
print(f"Status now: {'Done' if walk.isCompleted() else 'Pending'}")
if next_task:
    print(f"Next occurrence created: {next_task.getName()} at {next_task.getTime()}")

# --- Conflict detection ---
print("\n=== Conflict Detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts found.")
