import re
import time

from config import (Colors, TERMINAL_HEIGHT, DEFAULT_TIMER_LENGTH)
from tasks import add_task


# Utilities

def clear_screen():
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


def get_tasks(tod_file_data):
    """Return list of task dicts from .tod file"""
    tasks = []
    tod_file_data = tod_file_data.split('\n')

    for task_text in tod_file_data:
        if task_text == '' or task_text[0] != '[':
            continue
        task_name = task_text[4:-7]
        time_spent = task_text[-5:-1]
        completed = True if task_text[1] == 'X' else False
        tasks.append({
            "name": task_name,
            "time_spent": time_spent,
            "completed": completed
        })

    return tasks


def get_last_mit(track_file_data):
    """Return recent MIT from track data"""
    last_data = track_file_data.rsplit('\n> ', 1)
    mit, _ = last_data[1].split('\n', 1)
    return mit


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
        if re.match('\d:[0-6]\d', time_spent):
            break
        elif re.match('[0-6]?\d', time_spent):
            time_spent = f"0:{time_spent.zfill(2)}"
            break
        elif time_spent == '' and default_time:
            return default_time
        elif time_spent == '':
            return '0:00'
        print('Please ensure your input matches `H:MM`.')
    return time_spent


# Helper Function

def start_new_task_list(mit_from_track: str = None):
    """Start new task list and return with new tasks"""
    tasks = []

    if mit_from_track is not None and ' (Completed)' not in mit_from_track:
        print(Colors.BLUE + 'MIT from Track:' + Colors.NORMAL)
        print(f'Task Name: {mit_from_track}')
        tasks = add_task(tasks, mit_from_track, '0:00')
        print()

    while True:
        task_name = task_name_input()
        if not task_name:
            break
        time_spent = '0:00'
        tasks = add_task(tasks, task_name, time_spent)

    return tasks


def print_all_tasks(tasks: list):
    """Print tasks to screen"""
    print('\n' + Colors.BLUE + 'TASKS:' + Colors.NORMAL + '\n')
    if len(tasks) == 0:
        print('No tasks.')
    for index, task in enumerate(tasks):
        text_color = Colors.GREEN if task['completed'] else Colors.NORMAL
        time_spent = (f" ({task['time_spent']})"
                      if task['time_spent'] != "0:00"
                      else '')
        print(f"{index}. {text_color}" +
              f"{task['name']}{time_spent}{Colors.NORMAL}")
    print()


# String Formatting

def format_seconds_to_time_spent(seconds: int):
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return f"{hours}:{minutes:02}"


def format_tasks_to_plaintext(tasks: list):
    """Return formatted tasks string"""
    formatted_data = ''

    for index, task in enumerate(tasks):
        completed = '[X]' if task["completed"] else '[ ]'
        formatted_data += (
            f"{completed} {task['name']} ({task['time_spent']})")
        if index != len(tasks) - 1:
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
            clear_screen()
            print_timer_details(task_name, timer_length, elapsed_seconds)
            time.sleep(1)
            elapsed_seconds += 1
        except KeyboardInterrupt:
            break

    if elapsed_seconds >= timer_length_seconds:
        alarm(5)
    clear_screen()


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
