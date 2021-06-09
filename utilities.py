import os
import re
import time

from config import (Colors, TERMINAL_HEIGHT, DEFAULT_TIMER_LENGTH)
import tasks


# Utilities

def cls():
    """Clear screen"""
    print('\n' * TERMINAL_HEIGHT)


def show_help():
    """Print help to screen."""
    print('\n' +
          f'{Colors.BLACK_ON_WHITE}tod: Plan and manage your daily tasks{Colors.NORMAL}\n'
          f'\n' +
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
    print()
    input('Press enter to continue...')
    cls()


# Getters/Setters

def load_data(filepath):
    """Return data from file to string"""
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def save_data(data, filepath):
    """Save data to file"""
    with open(filepath, 'w') as f:
        f.write(data)


def set_env_variables():
    env_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env')
    env_data = load_data(env_path)
    for line in env_data.split('\n'):
        if not line: 
            continue
        k, v = line.split('=', 1)
        os.environ[k] = v


def parse_tasks(tod_file_data):
    """Return list of task dicts from .tod file"""
    active_tasks = []
    tod_file_data = tod_file_data.split('\n')

    for task_text in tod_file_data:
        if task_text.strip() == '':
            continue
        elif task_text[0] != '[':
            active_tasks[-1]["notes"] += task_text
            continue
        task_name = task_text[4:-7]
        time_spent = task_text[-5:-1]
        completed = True if task_text[1] == 'X' else False
        active_tasks.append({
            "name": task_name,
            "time_spent": time_spent,
            "notes": "",
            "completed": completed
        })

    return active_tasks


# Input Validation

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


def task_time_input(default_time: str = None):
    """Validate task time input"""
    while True:
        time_spent = input('Task Time: ')
        if re.match(r'\d:[0-6]\d', time_spent):
            break
        elif re.match(r'[0-6]?\d', time_spent):
            time_spent = f"0:{time_spent.zfill(2)}"
            break
        elif time_spent == '' and default_time:
            return default_time
        elif time_spent == '':
            return '0:00'
        print('Please ensure your input matches `H:MM`.')
    return time_spent


# Helper Function

def start_new_task_list():
    """Start new task list and return with new tasks"""
    active_tasks = []

    while True:
        task_name = task_name_input()
        if not task_name:
            break
        time_spent = '0:00'
        active_tasks = tasks.add(active_tasks, task_name, time_spent)

    return active_tasks


def print_all_tasks(active_tasks: list[dict]):
    """Print tasks to screen"""
    print('\n' + Colors.BLUE + 'TASKS:' + Colors.NORMAL + '\n')
    if len(active_tasks) == 0:
        print('No tasks.')
    for index, task in enumerate(active_tasks):
        color = Colors.GREEN if task['completed'] else Colors.NORMAL
        time_spent = (f" ({task['time_spent']})"
                      if task['time_spent'] != "0:00"
                      else '')
        notes = task.get('notes', '')
        notes = notes[0:40] + '...' if len(notes) > 40 else notes
        print(f"{index}. {color}{task['name']}{time_spent}{Colors.NORMAL}" +
              f" {Colors.GRAY}{notes}{Colors.NORMAL}")
    print()


# String Formatting

def format_seconds_to_time_spent(seconds: int):
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return f"{hours}:{minutes:02}"


def format_tasks_to_plaintext(active_tasks: list[dict]):
    """Return formatted tasks string"""
    formatted_data = ''

    for index, task in enumerate(active_tasks):
        completed = '[X]' if task["completed"] else '[ ]'
        formatted_data += (
            f"{completed} {task['name']} ({task['time_spent']})")
        if index != len(active_tasks) - 1:
            formatted_data += '\n'

    return formatted_data


# Timer

def spend_time_on_task(task_name):
    """Return time spent on task"""
    print(Colors.WHITE + 'Default timer length is: ' +
          Colors.RED + DEFAULT_TIMER_LENGTH + Colors.NORMAL + '\n')
    timer_length = task_time_input(DEFAULT_TIMER_LENGTH)

    timestamp_before_timer = int(time.time())
    timer(task_name, timer_length)
    timestamp_after_timer = int(time.time())

    return timestamp_after_timer - timestamp_before_timer


def timer(task_name, timer_length: str):
    timer_length_seconds = convert_time_spent_to_seconds(timer_length)

    elapsed_seconds = 0
    while elapsed_seconds <= timer_length_seconds:
        try:
            cls()
            print_timer_details(task_name, timer_length, elapsed_seconds)
            time.sleep(1)
            elapsed_seconds += 1
        except KeyboardInterrupt:
            break

    if elapsed_seconds >= timer_length_seconds:
        alarm(5)
    cls()


def convert_time_spent_to_seconds(length: str):
    hours, minutes = length.split(':')
    return (int(hours) * 60 + int(minutes)) * 60


def print_timer_details(task_name, timer_length, elapsed_seconds):
    print(Colors.YELLOW + task_name + Colors.NORMAL + '\n')
    print(f'Timer Length: {Colors.GREEN}{timer_length}:00{Colors.NORMAL}')
    print(f'Elapsed Time: {elapsed_seconds // 3600}:' +
          f'{((elapsed_seconds // 60) % 60):02}:' +
          f'{(elapsed_seconds % 60):02} \n')
    print(Colors.WHITE + 'Press `Ctrl + C` to stop the timer' +
          Colors.NORMAL + '\n')


def alarm(repetitions: int):
    try:
        for repetition in range(repetitions):
            for i in range(5):
                print('\a', end='', flush=True)
                time.sleep(.1)
            time.sleep(1.5)
    except KeyboardInterrupt:
        pass
