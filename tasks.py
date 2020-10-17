def add_task(tasks, task_name, timebox: str, index=None):
    """Return tasks with task inserted at index"""
    if not index:
        index = len(tasks)
    tasks.insert(index, (task_name, timebox, False))
    return tasks


def set_completion(tasks, index):
    """Return tasks with task completion flipped"""
    task_name, timebox, completed = tasks[index]
    tasks[index] = (task_name, timebox, not completed)
    return tasks


def delete_task(tasks, index):
    """Return tasks with task at index removed"""
    del tasks[index]
    return tasks


def update_task(tasks, task_name, timebox: str, index):
    """Return tasks with task at index updated"""
    tasks[index] = (task_name, timebox, False)
    return tasks


def move_task(tasks: list, from_index: int, to_index: int):
    """Return tasks with tasks rearranged by index"""
    tasks.insert(to_index, tasks.pop(from_index))
    return tasks


def reduce_tasks(tasks: list):
    """Return tasks with completed tasks removed"""
    tasks = [task for task in tasks if not task[2]]
    return tasks
