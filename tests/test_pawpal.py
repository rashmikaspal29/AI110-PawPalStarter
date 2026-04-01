from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete():
    task = Task("Morning Walk", "Walk around the block", "08:00", "daily", "high", 30)
    task.mark_complete()
    assert task.isCompleted() == True


def test_add_task():
    pet = Pet("Buddy", 3, "dog")
    assert len(pet.getTasks()) == 0
    pet.addTask(Task("Morning Walk", "Walk around the block", "08:00", "daily", "high", 30))
    assert len(pet.getTasks()) == 1


# --- Sorting Correctness ---

def test_sort_by_time_returns_chronological_order():
    pet = Pet("Buddy", 3, "dog")
    pet.addTask(Task("Evening Feed", "Kibble", "18:00", "daily", "medium", 10))
    pet.addTask(Task("Noon Walk", "Short walk", "12:00", "daily", "high", 20))
    pet.addTask(Task("Morning Walk", "Long walk", "08:00", "daily", "high", 30))
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.getTime() for t in sorted_tasks]
    assert times == sorted(times)


def test_sort_by_time_single_task():
    pet = Pet("Luna", 2, "cat")
    pet.addTask(Task("Feeding", "Milk", "10:00", "daily", "high", 10))
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    assert len(scheduler.sort_by_time()) == 1


# --- Recurrence Logic ---

def test_daily_task_creates_next_occurrence():
    task = Task("Morning Walk", "Walk", "08:00", "daily", "high", 30)
    next_task = task.mark_complete()
    assert task.isCompleted() == True
    assert next_task is not None
    assert next_task.getName() == "Morning Walk"
    assert next_task.isCompleted() == False


def test_weekly_task_creates_next_occurrence():
    task = Task("Bath", "Weekly bath", "10:00", "weekly", "medium", 20)
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.getFrequency() == "weekly"


def test_non_recurring_task_returns_none():
    task = Task("Vet Visit", "Annual checkup", "09:00", "once", "high", 60)
    next_task = task.mark_complete()
    assert next_task is None


# --- Conflict Detection ---

def test_detect_conflicts_flags_same_time():
    pet = Pet("Buddy", 3, "dog")
    pet.addTask(Task("Morning Walk", "Walk", "08:00", "daily", "high", 30))
    pet.addTask(Task("Playtime", "Toys", "08:00", "weekly", "low", 20))
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_no_conflict():
    pet = Pet("Buddy", 3, "dog")
    pet.addTask(Task("Morning Walk", "Walk", "08:00", "daily", "high", 30))
    pet.addTask(Task("Feeding", "Kibble", "10:00", "daily", "medium", 10))
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_no_tasks_no_conflicts():
    pet = Pet("Luna", 2, "cat")
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


# --- Filter Tasks ---

def test_filter_by_pet_name():
    pet1 = Pet("Buddy", 3, "dog")
    pet2 = Pet("Luna", 2, "cat")
    pet1.addTask(Task("Walk", "Walk", "08:00", "daily", "high", 30))
    pet2.addTask(Task("Feed", "Feed", "09:00", "daily", "high", 10))
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet1)
    owner.addPet(pet2)
    scheduler = Scheduler(owner)
    results = scheduler.filter_tasks(pet_name="Buddy")
    assert len(results) == 1
    assert results[0].getName() == "Walk"


def test_filter_by_completion_status():
    pet = Pet("Buddy", 3, "dog")
    t1 = Task("Walk", "Walk", "08:00", "daily", "high", 30)
    t2 = Task("Feed", "Feed", "09:00", "daily", "medium", 10)
    t1.mark_complete()
    pet.addTask(t1)
    pet.addTask(t2)
    owner = Owner("Rashmi", "", "")
    owner.addPet(pet)
    scheduler = Scheduler(owner)
    pending = scheduler.filter_tasks(completed=False)
    assert len(pending) == 1
    assert pending[0].getName() == "Feed"
