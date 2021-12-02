import argparse
import os

from menu import main_menu
from utilities import cls, load_data, parse_tasks, set_env_variables

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Plan and manage daily tasks.')
    argparser.add_argument('--pomodoro', '-p', action='store_true', help='Add 5 minute breaks to end of completed task timers')
    args = argparser.parse_args()
    set_env_variables()
    try:
        data = load_data(os.getenv('TOD_FP'))
        active_tasks, first_list = parse_tasks(data)
    except FileNotFoundError:
        first_list = 'MAIN'
        active_tasks = {first_list: list()}

    cls()
    main_menu(active_tasks, first_list, args)
