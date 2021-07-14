import os
import re
import sys

import tasks
from utilities import Colors as C
from utilities import cls, convert_time_spent_to_seconds, format_seconds_to_time_spent, format_tasks_to_plaintext, \
    print_all_tasks, save_data, show_help, spend_time_on_task, start_new_task_list, task_name_input, \
    task_number_input, task_time_input


def main_menu(active_tasks: list[dict]):
    verbose = False
    while True:
        data = format_tasks_to_plaintext(active_tasks)
        save_data(data, os.getenv('TOD_FP'))

        print_all_tasks(active_tasks, verbose)
        raw_command = input('► ').lower()

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
            time_spent_in_seconds = spend_time_on_task(task['name'])
            prev_time_spent_in_seconds = convert_time_spent_to_seconds(task['time_spent'])
            total_time_spent = prev_time_spent_in_seconds + time_spent_in_seconds
            formatted_time_spent = format_seconds_to_time_spent(total_time_spent)
            updated_task = {**task, 'time_spent': formatted_time_spent}
            tasks.update(active_tasks, updated_task, selected_number)
            print(C.PURPLE + 'Elapsed time added.' + C.NORMAL)
        elif command == 'a':
            task_name, task_notes = task_name_input()
            cls()
            new_task = {
                'name': task_name,
                'time_spent': '0:00',
                'notes': task_notes,
                'completed': False
            }
            active_tasks = tasks.add(active_tasks, new_task, selected_number)
            print(C.PURPLE + 'Task added.' + C.NORMAL)
        elif command == 'c':
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            cls()
            active_tasks = tasks.set_completion(active_tasks, selected_number)
            print(C.PURPLE + 'Task updated.' + C.NORMAL)
        elif command == 'dd':
            active_tasks = []
            print(C.PURPLE + 'Tasks deleted.' + C.NORMAL)
        elif command == 'd':
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            cls()
            active_tasks = tasks.delete(active_tasks, selected_number)
            print(C.PURPLE + 'Task deleted.' + C.NORMAL)
        elif command == 'e':
            if number_of_tasks is 0:
                print(C.PURPLE + 'No tasks to edit.' + C.NORMAL)
                continue
            if selected_number is None:
                print_all_tasks(active_tasks)
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
        elif command == 'm':
            if number_of_tasks is 0:
                print(C.PURPLE + 'No tasks to move.' + C.NORMAL)
                continue
            print_all_tasks(active_tasks)
            if selected_number is None:
                selected_number = task_number_input(number_of_tasks)
            if not dest_number:
                dest_number = int(input(f'Move task {selected_number} to where? '))
            cls()
            active_tasks = tasks.move(active_tasks, selected_number, dest_number)
            print(C.PURPLE + 'Tasks updated.' + C.NORMAL)
        elif command == 'n':
            verbose = True if not verbose else False
            print(C.PURPLE + 'Notes are now fully visible.' + C.NORMAL)
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
