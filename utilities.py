import math
import re
from time import sleep


class Colors:
    WHITE = "\033[97m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    NORMAL = '\033[0m'


def cls():
    """Clear screen"""
    print('\n' * 40)


def show_help():
    """Print help to screen."""
    print('\n' +
          'tod: Plan and manage your daily tasks\n'
          '\n' +
          'CLI Commands:\n' +
          '  [n]     Start focus time and timer for task `n`\n' +
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


def load_data(fp):
    """Return data from file to string"""
    with open(fp, 'r') as f:
        data = f.read()
    return data


def save_data(data, fp):
    """Save data to file"""
    with open(fp, 'w') as f:
        f.write(data)


def get_tasks(data):
    """Return list of task tuples from file"""
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
    """Return formatted tasks for plaintext"""
    formatted_data = ''

    for task in tasks:
        task_name, timebox, completed = task
        completed = '[X]' if completed else '[ ]'
        formatted_data += f'{completed} {task_name} ({timebox})'
        formatted_data += '\n'

    return formatted_data


def get_mit(data):
    """Return recent MIT from track data"""
    last_data = data.rsplit('\n> ', 1)
    mit, _ = last_data[1].split('\n', 1)
    return mit


def task_number_input(length: int):
    """Validate task number input"""
    number = input('Which task: ')
    if number == '' or int(number) >= length:
        print(Colors.RED + "No such task." + Colors.NORMAL)
        return None
    return int(number)


def task_name_input(prev_name=None):
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


def timer(task: tuple):
    task_name, timebox, completed = task

    hours, minutes = timebox.split(':')
    timebox_s = ((int(hours) * 60) + int(minutes)) * 60
    elapsed_s = 0

    while elapsed_s <= timebox_s:
        cls()
        print(Colors.YELLOW + task_name + Colors.NORMAL + '\n')
        print('Elapsed Time: ' +
              f'{elapsed_s // 3600}:' +
              f'{(elapsed_s // 60):02}:' +
              f'{(elapsed_s % 60):02}' + '\n')
        print(Colors.WHITE +
              'Press `Ctrl + C` to stop the timer' +
              Colors.NORMAL + '\n')
        try:
            sleep(1)
            elapsed_s += 1
        except KeyboardInterrupt:
            break

    if elapsed_s >= timebox_s:
        print('\a')
        return task_name, "0:00", True

    seconds = timebox_s - elapsed_s
    hours, minutes = divmod(math.ceil(seconds / 60), 60)
    return task_name, f"{hours:01}:{minutes:02}", False
