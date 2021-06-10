import os
import re
import sys

import tasks
from utilities import Colors as C
from utilities import cls, convert_time_spent_to_seconds, format_seconds_to_time_spent, format_tasks_to_plaintext, \
    print_all_tasks, save_data, show_help, spend_time_on_task, start_new_task_list, task_name_input, \
    task_number_input, task_time_input


def main_menu(active_tasks: list[dict], archive: str):
    verbose = False
    while True:
        print_all_tasks(active_tasks, verbose)
        command = input('► ').lower()

        cls()
        number = (int(command[1:])
                  if re.match(r'[A-Za-z]\d+', command)
                  else None)
        if number is not None and number >= len(active_tasks):
            print(C.RED + "No such task.\n" + C.NORMAL)
            continue

        if command == '':
            show_help()
        elif re.match(r'\d+$', command):
            number = int(command)
            try:
                task = active_tasks[number]
            except IndexError:
                print(C.RED + "No such task.\n" + C.NORMAL)
                continue                
            time_spent_in_seconds = spend_time_on_task(task['name'])
            prev_time_spent_in_seconds = convert_time_spent_to_seconds(task['time_spent'])
            total_time_spent = prev_time_spent_in_seconds + time_spent_in_seconds
            formatted_time_spent = format_seconds_to_time_spent(total_time_spent)
            updated_task = {**task, 'time_spent': formatted_time_spent}
            tasks.update(active_tasks, updated_task, number)
            cls()
            print(C.PURPLE + 'Elapsed time added.' + C.NORMAL)
        elif 'a' in command[0]:
            task_name, task_notes = task_name_input()
            new_task = {
                'name': task_name,
                'time_spent': '0:00',
                'notes': task_notes,
                'completed': False
            }
            active_tasks = tasks.add(active_tasks, new_task, number)
            cls()
            print(C.PURPLE + 'Task added.' + C.NORMAL)
        elif 'c' in command[0]:
            if number is None:
                number = task_number_input(len(active_tasks))
            active_tasks = tasks.set_completion(active_tasks, number)
            cls()
            print(C.PURPLE + 'Task updated.' + C.NORMAL)
        elif len(command) == 2 and command == 'dd':
            active_tasks = []
            cls()
            print(C.PURPLE + 'Tasks deleted.' + C.NORMAL)
        elif 'd' in command[0]:
            if number is None:
                number = task_number_input(len(active_tasks))
            active_tasks = tasks.delete(active_tasks, number)
            cls()
            print(C.PURPLE + 'Task deleted.' + C.NORMAL)
        elif 'e' in command[0]:
            if number is None:
                print_all_tasks(active_tasks)
                number = task_number_input(len(active_tasks))
                cls()
            task = active_tasks[number]
            print('\n' + C.BLUE + "Original Task:" + C.NORMAL)
            print(f"\n{task['name']} ({task['time_spent']})\n{task.get('notes')}\n")
            updated_task_name, updated_task_notes = task_name_input(task['name'])
            updated_time_spent = task_time_input(task['time_spent'])
            updated_task = {**task,
                            'name': updated_task_name,
                            'notes': updated_task_notes,
                            'time_spent': updated_time_spent}
            active_tasks = tasks.update(active_tasks, updated_task, number)
            cls()
            print(C.PURPLE + 'Task updated.' + C.NORMAL)
        elif 'h' in command[0]:
            show_help()
        elif 'm' in command[0]:
            print_all_tasks(active_tasks)
            if number is None:
                number = task_number_input(len(active_tasks))
            to_number = int(input(f'Move task {number} to where? '))
            active_tasks = tasks.move(active_tasks, number, to_number)
            cls()
            print(C.PURPLE + 'Tasks updated.' + C.NORMAL)
        elif 'n' in command[0]:
            verbose = True if not verbose else False
            cls()
            print(C.PURPLE + 'Notes are now fully visible.' + C.NORMAL)
        elif 'r' in command[0]:
            active_tasks = tasks.reduce(active_tasks)
            print(C.PURPLE + 'Tasks reduced.' + C.NORMAL)
        elif 's' in command[0]:
            print('Starting new task list...\n')
            active_tasks, archive = start_new_task_list(active_tasks, archive)
            cls()
        elif 'x' in command[0]:
            if input('Are you sure?').lower()[0] == 'y':
                archive = ''
            cls()

        data = format_tasks_to_plaintext(active_tasks) + archive
        save_data(data, os.getenv('TOD_FP'))

        if 'q' in command[0]:
            sys.exit()
        else:
            print(C.WHITE + "Try 'help' for more information." + C.NORMAL)
