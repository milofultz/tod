import math
import os
import re
import time
from typing import Tuple

from config import (Colors, TERMINAL_HEIGHT, DEFAULT_TIMER_LENGTH)
import tasks


CHECK_DELIMITER = re.compile(r'\[([Xx\s])]\s(.*)\s\((\d+:\d{2})\)')
LIST_DELIMITER = re.compile(r'\[([A-Z0-9\s]{2,})+]')


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
          '  [n]       Start focus time and timer for task `n`\n' +
          '  aa        (Add) multiple new tasks to end of list\n' +
          '  al        (A)dd a (L)ist\n' +
          '  a[n]      (A)dd task at index `n`\n' +
          '  c[n]      Set (C)ompletion of task `n`\n' +
          '  d[n]      (D)elete task `n`\n' +
          '  dd        Delete all tasks\n' +
          '  dl        Delete list\n' +
          '  e[n]      (E)dit task `n`\n' +
          '  h         Print this (H)elp menu\n' +
          '  l         Go to another (L)ist\n' +
          '  m[n]      (M)ove task `n`\n' +
          '  m[n]:[x]  (M)ove task `n` to position `x`\n' +
          '  n         Toggle full (N)otes when printing tasks\n'
          '  q         (Q)uit\n' +
          '  r         (R)educe/remove the completed tasks from the list\n' +
          '  s         (S)tart a new set of daily tasks\n')
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
    """Set filepath to user's .tod file"""
    env_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env')
    env_data = load_data(env_path)
    os.environ['TOD_FP'] = os.path.join(os.path.expanduser('~'), '.tod')
    for line in env_data.split('\n'):
        if not line:
            continue
        k, v = line.split('=', 1)
        os.environ[k] = v
    if not os.path.isfile(os.getenv('TOD_FP')):
        with open(os.getenv('TOD_FP'), 'x') as f:
            pass


def parse_tasks(tod_file_data: str) -> (dict[str, list], str):
    """Return list of task dicts from .tod file"""
    current_list = 'MAIN'
    active_tasks = {current_list: list()}
    tod_file_data = tod_file_data.split('\n')
    first_list = ''

    for line in tod_file_data:
        line = line.strip()
        if match := LIST_DELIMITER.match(line):
            current_list = match.groups()[0]
            if not first_list:
                first_list = current_list
            if not active_tasks.get(current_list):
                active_tasks[current_list] = list()
            else:
                raise RuntimeError(f"There is already a list named {current_list}. Change that list name and try again.")
        elif match := CHECK_DELIMITER.match(line):
            completed, task_name, time_spent = match.groups()
            # task_name = line[4:-7]
            # time_spent = line[-5:-1]
            active_tasks[current_list].append({
                "name": task_name,
                "time_spent": time_spent,
                "notes": "",
                "completed": completed == 'X'
            })
        elif line != "":
            active_tasks[current_list][-1]["notes"] += line

    return active_tasks, first_list or 'MAIN'


# Input Validation

def list_number_input(length: int):
    """Validate task number input"""
    number = ''
    while number == '':
        try:
            number = int(input('Which list: '))
        except ValueError:
            cls()
            print(Colors.RED + "Please enter a number." + Colors.NORMAL)
            number = ''
    if int(number) >= length:
        return None
    else:
        return int(number)


def task_number_input(length: int):
    """Validate task number input"""
    number = ''
    while number == '':
        try:
            number = int(input('Which task: '))
        except ValueError:
            cls()
            print(Colors.RED + "Please enter a number." + Colors.NORMAL)
            number = ''
    if int(number) >= length:
        return None
    else:
        return int(number)


def list_name_input() -> str or None:
    """Validate list name input"""
    list_input = input('List Name ▶ ').strip()
    if list_input == '':
        return None
    return list_input.upper()


def task_name_input(prev_name=None, prev_notes='') -> Tuple[str, str]:
    """Validate task name input"""
    task_input = input('Task Name :: Notes ▶ ').strip()
    if task_input == '' and prev_name:
        task_name = prev_name
        task_notes = prev_notes
    elif '::' == task_input[:2]:
        task_name = prev_name
        task_notes = task_input[2:]
    elif '::' == task_input[-2:]:
        task_name = task_input[:-2]
        task_notes = prev_notes
    elif '::' in task_input:
        task_name, task_notes = task_input.split('::', 1)
    else:
        task_name = task_input
        task_notes = prev_notes
    return task_name.strip(), task_notes.strip()


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

def start_new_task_list() -> list[dict]:
    """Start new task list and return with new tasks"""
    active_tasks = []

    while True:
        task_name, task_notes = task_name_input()
        if not task_name:
            break
        new_task = {
            'name': task_name,
            'time_spent': '0:00',
            'notes': task_notes,
            'completed': False
        }
        active_tasks = tasks.add(active_tasks, new_task)

    return active_tasks


def print_all_lists(task_lists: dict[str, list]):
    """Print lists to screen"""
    print('\n' + Colors.BLUE + 'LISTS:' + Colors.NORMAL + '\n')
    for index, task_list in enumerate(task_lists.keys()):
        print(f"{index}. {task_list}")
    print()


def print_all_tasks(current_list: str, active_tasks: list[dict], verbose: bool = False):
    """Print tasks to screen"""
    print('\n' + Colors.BLUE + f'TASKS in {current_list} list:' + Colors.NORMAL + '\n')
    if len(active_tasks) == 0:
        print('No tasks.')
    for index, task in enumerate(active_tasks):
        color = Colors.GREEN if task['completed'] else Colors.NORMAL
        time_spent = (f" ({task['time_spent']})"
                      if task['time_spent'] != "0:00"
                      else '')
        notes = task.get('notes', '')
        if not verbose:
            notes = notes[0:40] + '...' if len(notes) > 40 else notes
        else:
            indent = int(math.log10(index)) if index != 0 else 0
            notes = f"\n   {indent * ' '}{notes}"
        print(f"{index}. {color}{task['name']}{time_spent}{Colors.NORMAL}" +
              f" {Colors.GRAY}{notes}{Colors.NORMAL}")
    print()


# String Formatting

def format_seconds_to_time_spent(seconds: int):
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return f"{hours}:{minutes:02}"


def format_all_tasks_to_plaintext(active_tasks: dict[str, list], current_list: str) -> str:
    """Return formatted tasks string"""
    formatted_data = ''

    for list_name, tasks_list in active_tasks.items():
        formatted_list = ''
        formatted_list += f'[{list_name}]\n'
        for task in tasks_list:
            completed = '[X]' if task["completed"] else '[ ]'
            formatted_list += f"{completed} {task['name']} ({task['time_spent']})"
            if notes := task.get('notes'):
                formatted_list += f"\n    {notes}"
            formatted_list += '\n'
        formatted_list += '\n'
        if list_name != current_list:
            formatted_data += formatted_list
        else:
            formatted_data = formatted_list + formatted_data

    return formatted_data


# Timer

def spend_time_on_task(task_name, task_notes, pomodoro: bool):
    """Return time spent on task"""
    print(Colors.WHITE + 'Default timer length is: ' +
          Colors.RED + DEFAULT_TIMER_LENGTH + Colors.NORMAL + '\n')
    timer_length = task_time_input(DEFAULT_TIMER_LENGTH)

    timestamp_before_timer = int(time.time())
    timer_completed = timer(task_name, task_notes, timer_length)
    timestamp_after_timer = int(time.time())

    if timer_completed and pomodoro:
        timer('Break', 'This is your pomodoro break. Get up and go do something else for a bit.', '0:05')

    return timestamp_after_timer - timestamp_before_timer


def timer(task_name, task_notes, timer_length: str) -> bool:
    timer_length_seconds = convert_time_spent_to_seconds(timer_length)

    timer_completed = False
    elapsed_seconds = 0
    while elapsed_seconds <= timer_length_seconds:
        try:
            cls()
            print_timer_details(task_name, task_notes, timer_length, elapsed_seconds)
            time.sleep(1)
            elapsed_seconds += 1
        except KeyboardInterrupt:
            break

    if elapsed_seconds >= timer_length_seconds:
        alarm(5)
        timer_completed = True

    cls()
    return timer_completed


def convert_time_spent_to_seconds(length: str):
    hours, minutes = length.split(':')
    return (int(hours) * 60 + int(minutes)) * 60


def print_timer_details(task_name, task_notes, timer_length, elapsed_seconds):
    print(Colors.YELLOW + task_name + Colors.NORMAL + '\n')
    if task_notes:
        print(Colors.GRAY + task_notes + Colors.NORMAL + '\n')
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
