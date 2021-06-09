def add(task_list, task_name, time_spent: str, index: int = None):
    """Return tasks with task inserted at index"""
    if index is None:
        index = len(task_list)
    new_task = {"name": task_name,
                "time_spent": time_spent,
                "completed": False}
    task_list.insert(index, new_task)
    return task_list


def set_completion(task_list, index):
    """Return tasks with task completion flipped"""
    task_list[index]["completed"] = not task_list[index]["completed"]
    return task_list


def delete(task_list, index):
    """Return tasks with task at index removed"""
    del task_list[index]
    return task_list


def update(task_list, task_name, time_spent: str, index):
    """Return tasks with task at index updated"""
    task_list[index]['name'] = task_name
    task_list[index]['time_spent'] = time_spent
    return task_list


def move(task_list, from_index, to_index):
    """Return tasks with tasks rearranged by index"""
    task_list.insert(to_index, task_list.pop(from_index))
    return task_list


def reduce(task_list):
    """Return tasks with completed tasks removed"""
    task_list = [task for task in task_list if not task["completed"]]
    return task_list
