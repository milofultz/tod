import os
import re
import sys

from tasks import (add_task, set_completion, delete_task,
                   update_task, move_task, reduce_tasks)
from utilities import (Colors, clear_screen, show_help,
                       load_data, save_data, format_tasks_to_plaintext,
                       task_number_input, task_name_input, task_time_input,
                       spend_time_on_task, convert_time_spent_to_seconds,
                       format_seconds_to_time_spent, get_last_mit,
                       start_new_task_list, print_all_tasks)


def main_menu(tasks: list):
    while True:
        print_all_tasks(tasks)
        command = input('► ').lower()

        clear_screen()
        number = (int(command[1:])
                  if re.match('[A-Za-z]\d+', command)
                  else None)
        if number is not None and number >= len(tasks):
            print(Colors.RED + "No such task.\n" + Colors.NORMAL)
            continue

        if command == '':
            show_help()
        elif re.match('\d+$', command):
            number = int(command)
            try:
                task = tasks[number]
            except IndexError:
                print(Colors.RED + "No such task.\n" + Colors.NORMAL)
                continue                
            time_spent_in_seconds = spend_time_on_task(task['name'])
            prev_time_spent_in_seconds = convert_time_spent_to_seconds(task['time_spent'])
            total_time_spent = prev_time_spent_in_seconds + time_spent_in_seconds
            formatted_time_spent = format_seconds_to_time_spent(total_time_spent)
            update_task(tasks,
                        task['name'],
                        formatted_time_spent,
                        number)
            clear_screen()
            print(Colors.PURPLE + 'Elapsed time added.' + Colors.NORMAL)
        elif 'a' in command[0]:
            task_name = task_name_input()
            tasks = add_task(tasks, task_name, '0:00', number)
            clear_screen()
            print(Colors.PURPLE + 'Task added.' + Colors.NORMAL)
        elif 'c' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            tasks = set_completion(tasks, number)
            clear_screen()
            print(Colors.PURPLE + 'Task updated.' + Colors.NORMAL)
        elif len(command) == 2 and command == 'dd':
            tasks = []
            clear_screen()
            print(Colors.PURPLE + 'Tasks deleted.' + Colors.NORMAL)
        elif 'd' in command[0]:
            if number is None:
                number = task_number_input(len(tasks))
            tasks = delete_task(tasks, number)
            clear_screen()
            print(Colors.PURPLE + 'Task deleted.' + Colors.NORMAL)
        elif 'e' in command[0]:
            if number is None:
                print_all_tasks(tasks)
                number = task_number_input(len(tasks))
                clear_screen()
            task = tasks[number]
            print('\n' + Colors.BLUE + "Original Task:" + Colors.NORMAL)
            print(f"\n{task['name']} ({task['time_spent']})\n")
            updated_task_name = task_name_input(task['name'])
            updated_time_spent = task_time_input(task['time_spent'])
            tasks = update_task(tasks, updated_task_name,
                                updated_time_spent, number)
            clear_screen()
            print(Colors.PURPLE + 'Task updated.' + Colors.NORMAL)
        elif 'h' in command[0]:
            show_help()
        elif 'm' in command[0]:
            print_all_tasks(tasks)
            if number is None:
                number = task_number_input(len(tasks))
            to_number = int(input(f'Move task {number} to where? '))
            tasks = move_task(tasks, number, to_number)
            clear_screen()
            print(Colors.PURPLE + 'Tasks updated.' + Colors.NORMAL)
        elif 'q' in command[0]:
            sys.exit()
        elif 'r' in command[0]:
            tasks = reduce_tasks(tasks)
            print(Colors.PURPLE + 'Tasks reduced.' + Colors.NORMAL)
        elif 's' in command[0]:
            print('Starting new task list...\n')
            try:
                track_data = load_data(os.getenv('TRACK_FP'))
                mit_from_track = get_last_mit(track_data)
                tasks = start_new_task_list(mit_from_track)
            except FileNotFoundError:
                tasks = start_new_task_list()
            clear_screen()
        else:
            print(Colors.WHITE + "Try 'help' for more information." +
                  Colors.NORMAL)

        data = format_tasks_to_plaintext(tasks)
        save_data(data, os.getenv('TOD_FP'))
