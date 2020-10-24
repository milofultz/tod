from config import Filepaths
from menu import main_menu
from utilities import clear_screen, load_data, get_tasks

if __name__ == "__main__":
    try:
        data = load_data(Filepaths.TOD)
        tasks = get_tasks(data)
    except FileNotFoundError:
        tasks = []

    clear_screen()
    main_menu(tasks)
