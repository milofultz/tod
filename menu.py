from argparse import Namespace
import os
import re
import sys
import time

import tasks
from utilities import Colors as C
from utilities import cls, convert_time_spent_to_seconds, format_seconds_to_time_spent, format_all_tasks_to_plaintext, \
    list_name_input, list_number_input, print_all_lists, print_all_tasks, save_data, show_help, spend_time_on_task, start_new_task_list, \
    task_name_input, task_number_input, task_time_input


def main_menu(task_lists: dict[str, list], current_list: str, arguments: Namespace):
    verbose = False
    active_tasks = task_lists.get(current_list)
    while True:
        task_lists[current_list] = active_tasks
        data = format_all_tasks_to_plaintext(task_lists, current_list)
        save_data(data, os.getenv('TOD_FP'))

        print_all_tasks(current_list, active_tasks, verbose)
        raw_command = input('► ')

        cls()
        parsed_command = re.match(r'([A-Za-z]*)(\d+)?:?(\d+)?', raw_command).groups()
        command, selected_number, dest_number = parsed_command
        if selected_number:
            selected_number = int(selected_number)
        if dest_number:
            dest_number = int(dest_number)
        number_of_tasks = len(active_tasks)
        if selected_number is not None \
                and selected_number >= number_of_tasks \
                and command != 'a':
            print(C.RED + "No such task.\n" + C.NORMAL)
            continue

        cls()

        if raw_command == '':
            show_help()
        elif not command and selected_number is not None:
            task = active_tasks[selected_number]
            time_spent_in_seconds = spend_time_on_task(task.get('name'), task.get('notes'), arguments.pomodoro)
            prev_time_spent_in_seconds = convert_time_spent_to_seconds(task.get('time_spent'))
            total_time_spent = prev_time_spent_in_seconds + time_spent_in_seconds
            formatted_time_spent = format_seconds_to_time_spent(total_time_spent)
            updated_task = {**task, 'time_spent': formatted_time_spent}
            tasks.update(active_tasks, updated_task, selected_number)
            print(C.PURPLE + 'Elapsed time added.' + C.NORMAL)
        elif command == 'aa':
            cls()
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
                active_tasks = tasks.add(active_tasks, new_task, selected_number)
            cls()
            print(C.PURPLE + 'Tasks added.' + C.NORMAL)
        elif command == 'al':
            cls()
            new_list_name = list_name_input()
            cls()
            if not new_list_name:
                print(C.RED + 'No name entered.' + C.NORMAL)
                continue
            task_lists[new_list_name] = list()
            current_list = new_list_name
            active_tasks = task_lists[current_list]
            print(C.PURPLE + 'List created.' + C.NORMAL)
        elif command == 'a':
            task_name, task_notes = task_name_input()
            cls()
            if not task_name:
                print(C.RED + 'Cannot add empty task.' + C.NORMAL)
                continue
            new_task = {
                'name': task_name,
                'time_spent': '0:00',
                'notes': task_notes,
                'completed': False
            }
            active_tasks = tasks.add(active_tasks, new_task, selected_number)
            print(C.PURPLE + 'Task added.' + C.NORMAL)
        elif command == 'b':
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            timestamp_before = int(time.time())
            current_number = selected_number
            current_task = active_tasks[selected_number]
            print(C.YELLOW + current_task.get('name') + C.NORMAL + '\n')
            if current_task.get('notes'):
                print(C.GRAY + current_task.get('notes') + C.NORMAL + '\n')
            print('Enter your new broken down tasks:\n')
            while True:
                current_number += 1
                task_name, task_notes = task_name_input()
                if not task_name:
                    break
                new_task = {
                    'name': task_name,
                    'time_spent': '0:00',
                    'notes': task_notes,
                    'completed': False
                }
                active_tasks = tasks.add(active_tasks, new_task, current_number)
            timestamp_after = int(time.time())
            time_spent_in_seconds = timestamp_after - timestamp_before
            prev_time_spent_in_seconds = convert_time_spent_to_seconds(current_task.get('time_spent'))
            total_time_spent = prev_time_spent_in_seconds + time_spent_in_seconds
            formatted_time_spent = format_seconds_to_time_spent(total_time_spent)
            updated_task = {**current_task, 'time_spent': formatted_time_spent}
            tasks.update(active_tasks, updated_task, selected_number)
            cls()
            print(C.PURPLE + 'Tasks added.' + C.NORMAL)
        elif command == 'c':
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            cls()
            if selected_number is not None:
                active_tasks = tasks.set_completion(active_tasks, selected_number)
                print(C.PURPLE + 'Task updated.' + C.NORMAL)
        elif command == 'dd':
            active_tasks = []
            print(C.PURPLE + 'Tasks deleted.' + C.NORMAL)
        elif command == 'dl':
            list_names = list(task_lists.keys())
            print_all_lists(list_names)
            selected_number = list_number_input(len(list_names))
            cls()
            selected_list = list_names[selected_number]
            del task_lists[selected_list]
            if selected_list == current_list:
                current_list = list_names[0]
            print(C.PURPLE + 'List deleted.' + C.NORMAL)
        elif command == 'd':
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            cls()
            active_tasks = tasks.delete(active_tasks, selected_number)
            print(C.PURPLE + 'Task deleted.' + C.NORMAL)
        elif command == 'e':
            if number_of_tasks == 0:
                print(C.PURPLE + 'No tasks to edit.' + C.NORMAL)
                continue
            if selected_number is None:
                print_all_tasks(current_list, active_tasks)
                selected_number = task_number_input(number_of_tasks)
                cls()
            task = active_tasks[selected_number]
            print('\n' + C.BLUE + "Original Task:" + C.NORMAL)
            name = task['name']
            notes = ': ' + task.get('notes') if task.get('notes') else ''
            time_spent = task['time_spent']
            print(f"\n{name}{notes}\n({time_spent})\n")
            updated_task_name, updated_task_notes = task_name_input(name, task['notes'])
            updated_time_spent = task_time_input(time_spent)
            cls()
            updated_task = {**task,
                            'name': updated_task_name,
                            'notes': updated_task_notes,
                            'time_spent': updated_time_spent}
            active_tasks = tasks.update(active_tasks, updated_task, selected_number)
            print(C.PURPLE + 'Task updated.' + C.NORMAL)
        elif command == 'h':
            show_help()
        elif command == 'l':
            print_all_lists(task_lists)
            list_names = task_lists.keys()
            selected_number = list_number_input(len(list_names))
            cls()
            current_list = list(list_names)[selected_number]
            active_tasks = task_lists.get(current_list)
            print(C.PURPLE + 'List selected.' + C.NORMAL)
        elif command == 'ml':
            if number_of_tasks == 0:
                print(C.PURPLE + 'No tasks to move.' + C.NORMAL)
                continue
            print_all_tasks(current_list, active_tasks)
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            cls()
            list_names = list(task_lists.keys())
            print_all_lists(list_names)
            destination_list_number = int(input(f'Move task {selected_number} to which list? '))
            destination_list = task_lists[list_names[destination_list_number]]
            cls()
            active_tasks, destination_list = tasks.move_to_list(active_tasks, destination_list, selected_number)
            task_lists[list_names[destination_list_number]] = destination_list
            print(C.PURPLE + 'Task moved.' + C.NORMAL)
        elif command == 'm':
            if number_of_tasks == 0:
                print(C.PURPLE + 'No tasks to move.' + C.NORMAL)
                continue
            print_all_tasks(current_list, active_tasks)
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            if dest_number is None:
                dest_number = int(input(f'Move task {selected_number} to where? '))
            cls()
            active_tasks = tasks.move(active_tasks, selected_number, dest_number)
            print(C.PURPLE + 'Tasks updated.' + C.NORMAL)
        elif command == 'n':
            verbose = True if not verbose else False
            message = 'Notes are now fully visible.' if verbose else 'Notes are now truncated.'
            print(C.PURPLE + message + C.NORMAL)
        elif command == 'q':
            sys.exit()
        elif command == 'r':
            active_tasks = tasks.reduce(active_tasks)
            print(C.PURPLE + 'Tasks reduced.' + C.NORMAL)
        elif command == 's':
            print('Starting new task list...\n')
            active_tasks = start_new_task_list()
            cls()
        else:
            print(C.WHITE + "Try 'help' for more information." + C.NORMAL)
