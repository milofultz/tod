from pathlib import Path
import re
import sys

from utilities import (cls, show_help, Colors, load_data, save_data,
                       get_tasks, format_tasks, get_mit,
                       task_number_input, task_name_input, task_time_input,
                       timer)
from tasks import (add_task, set_completion, delete_task, update_task,
                   move_task, reduce_tasks)


# Constants

TOD_FP = str(Path.home()) + '/.tod'
TRACK_FP = str(Path.home()) + '/.track'
POMODORO_TIME = '0:25'


# Actions

def show_tasks(tasks: list):
    """Print tasks to screen"""
    print('\n' + Colors.BLUE + 'TASKS:' + Colors.NORMAL + '\n')
    if len(tasks) == 0:
        print('No tasks.')
    for index, task in enumerate(tasks):
        task_name, time_spent, completed = task
        if time_spent == '0:00':
            time_spent = ''
        else:
            time_spent = f'({time_spent})'
        text_color = Colors.GREEN if completed else Colors.NORMAL
        print(f"{index}. {text_color}{task_name} {time_spent}{Colors.NORMAL}")
    print('\n')


def start(mit: str = None):
    """Start new task list and return with new tasks"""
    tasks = []

    if mit is not None and ' (Completed)' not in mit:
        print()
        print(Colors.BLUE + 'MIT from Track:\n' + Colors.NORMAL)
        print(f'Task Name: {mit}')
        time_spent = '0:00'
        tasks = add_task(tasks, mit, time_spent)

    while True:
        print()
        task_name = task_name_input()
        if not task_name:
            break
        time_spent = '0:00'
        tasks = add_task(tasks, task_name, time_spent)
    return tasks


if __name__ == "__main__":
    try:
        data = load_data(TOD_FP)
        tasks = get_tasks(data)
    except FileNotFoundError:
        tasks = []

    cls()
    while True:
        show_tasks(tasks)
        command = input('► ').lower()

        cls()
        number = (int(command[1:]) 
                  if re.match('[A-Za-z]\d+', command) 
                  else None)
        if number is not None and number >= len(tasks):
            print(Colors.RED + "No such task.\n" + Colors.NORMAL)
            continue

        if not command:
            print(Colors.WHITE + "Try 'help' for more information.\n" + Colors.NORMAL)
        elif re.match('\d+$', command):
            number = int(command)
            if tasks[number][2]:
                cls()
                print(Colors.GREEN + 'Task already complete.\n' + Colors.NORMAL)
                continue
            print(Colors.WHITE +
                  'Default timer length is: ' +
                  Colors.RED + POMODORO_TIME + Colors.NORMAL)
            length = task_time_input(POMODORO_TIME)
            task = timer(tasks[number], length)
            tasks[number] = task
            cls()
            print(Colors.PURPLE + 'Elapsed time added.\n' + Colors.NORMAL)
        elif 'a' in command[0]:
            print()
            task_name = task_name_input()
            tasks = add_task(tasks, task_name, '0:00', number)
            cls()
            print(Colors.PURPLE + 'Task added.\n' + Colors.NORMAL)
        elif 'c' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            if number is not None:
                tasks = set_completion(tasks, number)
                cls()
                print(Colors.PURPLE + 'Task updated.\n' + Colors.NORMAL)
        elif len(command) == 2 and command == 'dd':
            tasks = []
            cls()
            print(Colors.PURPLE + 'Tasks deleted.\n' + Colors.NORMAL)
        elif 'd' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            if number is not None:
                tasks = delete_task(tasks, number)
                cls()
                print(Colors.PURPLE + 'Task deleted.\n' + Colors.NORMAL)
        elif 'e' in command[0]:
            if number is None:
                show_tasks(tasks)
                number = task_number_input(len(tasks))
                cls()
            if number is not None:
                task_name, time_spent, completed = tasks[number]
                print('\n' + Colors.BLUE + "Original Task:" + Colors.NORMAL)
                print(f"\n{task_name} ({time_spent})\n")
                task_name = task_name_input(task_name)
                time_spent = task_time_input(time_spent)
                tasks = update_task(tasks, task_name, time_spent,
                                    completed, number)
                cls()
                print(Colors.PURPLE + 'Task updated.\n' + Colors.NORMAL)
        elif 'h' in command[0]:
            show_help()
        elif 'm' in command[0]:
            show_tasks(tasks)
            if number is None:
                number = task_number_input(len(tasks))
            to_number = int(input(f'Move task {number} to where? '))
            tasks = move_task(tasks, number, to_number)
            cls()
            print(Colors.PURPLE + 'Tasks updated.\n' + Colors.NORMAL)
        elif 'q' in command[0]:
            sys.exit()
        elif 'r' in command[0]:
            tasks = reduce_tasks(tasks)
            print(Colors.PURPLE + 'Tasks reduced.\n' + Colors.NORMAL)
        elif 's' in command[0]:
            print('Starting new task list...')
            try:
                track_data = load_data(TRACK_FP)
                mit = get_mit(track_data)
                tasks = start(mit)
            except FileNotFoundError:
                tasks = start()
            cls()
        else:
            print(Colors.WHITE + "Try 'help' for more information.\n" + Colors.NORMAL)

        data = format_tasks(tasks)
        save_data(data, TOD_FP)
