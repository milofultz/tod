import os

from menu import main_menu
from utilities import clear_screen, load_data, get_tasks, set_env_variables

if __name__ == "__main__":
    set_env_variables()
    try:
        data = load_data(os.getenv('TOD_FP'))
        tasks = get_tasks(data)
    except FileNotFoundError:
        tasks = []

    clear_screen()
    main_menu(tasks)
