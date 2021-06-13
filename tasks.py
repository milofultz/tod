def add(active_tasks: list[dict], new_task: dict, index: int = None):
    """Return tasks with task inserted at index"""
    if index is None:
        index = len(active_tasks)
    else:
        index = min(len(active_tasks), index)
    active_tasks.insert(index, new_task)
    return active_tasks


def set_completion(active_tasks, index):
    """Return tasks with task completion flipped"""
    active_tasks[index]["completed"] = not active_tasks[index]["completed"]
    return active_tasks


def delete(active_tasks, index):
    """Return tasks with task at index removed"""
    del active_tasks[index]
    return active_tasks


def update(active_tasks, updated_task: dict, index):
    """Return tasks with task at index updated"""
    active_tasks[index] = updated_task
    return active_tasks


def move(active_tasks, from_index, to_index):
    """Return tasks with tasks rearranged by index"""
    active_tasks.insert(to_index, active_tasks.pop(from_index))
    return active_tasks


def reduce(active_tasks):
    """Return tasks with completed tasks removed"""
    active_tasks = [task for task in active_tasks if not task["completed"]]
    return active_tasks
