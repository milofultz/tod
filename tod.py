import os

from menu import main_menu
from utilities import cls, load_data, parse_tasks, set_env_variables

if __name__ == "__main__":
    set_env_variables()
    try:
        data = load_data(os.getenv('TOD_FP'))
        active_tasks = parse_tasks(data)
    except FileNotFoundError:
        active_tasks = []

    cls()
    main_menu(active_tasks)
