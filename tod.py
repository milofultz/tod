# TRACK INTEGRATION
# track will read from the file
# if tasks exist, when starting main loop, ask if user wants to add
# accomplishments from tod file of date YYYYMMDD

from pathlib import Path
import re
import sys


# Constants

WHITE = "\033[97m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BLUE = '\033[94m'
PURPLE = '\033[95m'
NORMAL = '\033[0m'
TOD_FP = str(Path.home()) + '/.tod'
TRACK_FP = str(Path.home()) + '/.track'


# Utilities

def cls():
    """Clear screen"""
    print('\n' * 40)


def load_data():
    """Load data from file"""
    with open(TOD_FP, 'r') as f:
        data = f.read()
    print(data, type(data))
    return data


def get_tasks(data: str):
    """Parse data from file"""
    tasks = []
    data = data.split('\n')

    for task in data:
        if task == '' or task[0] != '[':
            continue
        task_name = task[4:-7]
        timebox = task[-5:-1]
        if task[1] == 'X':
            completed = True
        else:
            completed = False
        tasks.append((task_name, timebox, completed))

    return tasks


def format_tasks(tasks: list):
    """Format tasks for plaintext"""
    formatted_data = ''

    for task in tasks:
        task_name, timebox, completed = task
        completed = '[X]' if completed else '[ ]'
        formatted_data += f'{completed} {task_name} ({timebox})'
        formatted_data += '\n'

    return formatted_data


def save_data(data):
    """Save data to file"""
    with open(TOD_FP, 'w') as f:
        f.write(data)


def show_help():
    """Print help to screen."""
    print('\n' +
          'tod: Plan and manage your daily tasks\n'
          '\n' +
          'CLI Commands:\n' +
          '  a[n]    (A)dd task at index `n`\n' +
          '  c[n]    Set (C)ompletion of task `n`\n' +
          '  d[n]    (D)elete task `n`\n' +
          '  dd      Delete all tasks\n' +
          '  e[n]    (E)dit task `n`\n' +
          '  h       Print this (H)elp menu\n' +
          '  m[n]    (M)ove task `n`\n' +
          '  q       (Q)uit\n' +
          '  r       (R)educe/remove the completed tasks from the list\n' +
          '  s       (S)tart a new set of daily tasks\n')


def task_number_input(length: int):
    """Validate task number input"""
    number = input('Which task: ')
    if number == '' or int(number) >= length:
        print(RED + "No such task." + NORMAL)
        return None
    return int(number)


def task_name_input(prev_name: str = None):
    """Validate task name input"""
    task_name = input('Task Name: ')
    if task_name == '' and prev_name:
        return prev_name
    return task_name


def task_time_input(prev_timebox: str = None):
    """Validate task time input"""
    while True:
        timebox = input('Task Time: ')
        if len(timebox) == 4 and re.match('\d:[0-6]\d', timebox):
            break
        elif timebox == '' and prev_timebox:
            return prev_timebox
        print('Please ensure your input matches `H:MM`.')
    return timebox


# Actions

def add_task(tasks: list,
             task_name: str,
             timebox: str,
             index: int = None):
    """Add task to task list"""
    if not index:
        index = len(tasks)
    tasks.insert(index, (task_name, timebox, False))
    return tasks


def set_completion(tasks: list, index: int):
    """Change completion status of task"""
    task_name, timebox, completed = tasks[index]
    tasks[index] = (task_name, timebox, not completed)
    return tasks


def delete_task(tasks: list, index: int):
    """Delete task from list"""
    del tasks[index]
    return tasks


def update_task(tasks: list, task_name: str, timebox: str, index: int):
    """Update task with new information"""
    tasks[index] = (task_name, timebox, False)
    return tasks


def move_task(tasks: list, from_index: int, to_index: int):
    """Move task to new position in list"""
    tasks.insert(to_index, tasks.pop(from_index))
    return tasks


def reduce_tasks(tasks: list):
    """Remove completed tasks from list"""
    tasks = [task for task in tasks if not task[2]]
    return tasks


def show_tasks(tasks: list):
    """Print tasks to screen"""
    print('\n' + BLUE + 'TASKS:' + NORMAL + '\n')
    if len(tasks) == 0:
        print('No tasks.')
    for index, task in enumerate(tasks):
        task_name, timebox, completed = task
        color = GREEN if completed else NORMAL
        print(f"{index}. {color}{task_name} ({timebox}){NORMAL}")
    print('\n')


def start():
    """Start new task list and add tasks"""
    tasks = []
    print()
    # pull MIT from /~.track and add at top
    while True:
        task_name = input('Task: ')
        if not task_name:
            break
        while True:
            timebox = input('Time: ')
            if len(timebox) == 4 and re.match('\d:[0-6]\d', timebox):
                break
            print('Please ensure your input matches `H:MM`.')
        tasks = add_task(tasks, task_name, timebox)
    return tasks


if __name__ == "__main__":
    try:
        data = load_data()
        tasks = get_tasks(data)
    except FileNotFoundError:
        tasks = []

    need_help = False
    error_msg = None
    cls()
    while True:
        show_tasks(tasks)
        command = input('Next action: ').lower()

        cls()
        number = int(command[1:]) if re.match('\d+', command[1:]) else None
        if number and number >= len(tasks):
            print(RED + "No such task.\n" + NORMAL)
            continue

        if not command:
            print(WHITE + "Try 'help' for more information.\n" + NORMAL)
        elif 'a' in command[0]:
            print()
            task_name = task_name_input()
            timebox = task_time_input()
            tasks = add_task(tasks, task_name, timebox, number)
            cls()
            print(PURPLE + 'Task added.\n' + NORMAL)
        elif 'c' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            if number is not None:
                tasks = set_completion(tasks, number)
                cls()
                print(PURPLE + 'Task updated.\n' + NORMAL)
        elif len(command) == 2 and command == 'dd':
            tasks = []
            cls()
            print(PURPLE + 'Tasks deleted.\n' + NORMAL)
        elif 'd' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            if number is not None:
                tasks = delete_task(tasks, number)
                cls()
                print(PURPLE + 'Task deleted.\n' + NORMAL)
        elif 'e' in command[0]:
            if number is None:
                show_tasks(tasks)
                number = task_number_input(len(tasks))
                cls()
            if number is not None:
                task_name, timebox, _ = tasks[number]
                print('\n' + BLUE + "Original Task:" + NORMAL)
                print(f"\n{task_name} ({timebox})\n")
                task_name = task_name_input(task_name)
                timebox = task_time_input(timebox)
                tasks = update_task(tasks, task_name, timebox, number)
                cls()
                print(PURPLE + 'Task updated.\n' + NORMAL)
        elif 'h' in command[0]:
            show_help()
        elif 'm' in command[0]:
            show_tasks(tasks)
            if number is None:
                number = task_number_input(len(tasks))
            to_number = int(input(f'Move task {number} to where? '))
            tasks = move_task(tasks, number, to_number)
            cls()
            print(PURPLE + 'Tasks updated.\n' + NORMAL)
        elif 'q' in command[0]:
            sys.exit()
        elif 'r' in command[0]:
            tasks = reduce_tasks(tasks)
            print(PURPLE + 'Tasks reduced.\n' + NORMAL)
        elif 's' in command[0]:
            print('Starting new task list...')
            tasks = start()
        else:
            print(WHITE + "Try 'help' for more information.\n" + NORMAL)

        data = format_tasks(tasks)
        save_data(data)
