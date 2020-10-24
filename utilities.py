import re
from time import sleep


class Colors:
    WHITE = "\033[97m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    NORMAL = '\033[0m'


def cls():
    """Clear screen"""
    print('\n' * 40)


def show_help():
    """Print help to screen."""
    print('\n' +
          'tod: Plan and manage your daily tasks\n'
          '\n' +
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


def load_data(fp):
    """Return data from file to string"""
    with open(fp, 'r') as f:
        data = f.read()
    return data


def save_data(data, fp):
    """Save data to file"""
    with open(fp, 'w') as f:
        f.write(data)


def get_tasks(data):
    """Return list of task tuples from file"""
    tasks = []
    data = data.split('\n')

    for task in data:
        if task == '' or task[0] != '[':
            continue
        task_name = task[4:-7]
        time_spent = task[-5:-1]
        if task[1] == 'X':
            completed = True
        else:
            completed = False
        tasks.append((task_name, time_spent, completed))

    return tasks


def format_tasks(tasks: list):
    """Return formatted tasks for plaintext"""
    formatted_data = ''

    for task in tasks:
        task_name, time_spent, completed = task
        completed = '[X]' if completed else '[ ]'
        formatted_data += f'{completed} {task_name} ({time_spent})'
        formatted_data += '\n'

    return formatted_data


def get_mit(data):
    """Return recent MIT from track data"""
    last_data = data.rsplit('\n> ', 1)
    mit, _ = last_data[1].split('\n', 1)
    return mit


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


def timer(task: tuple, timer_length: str):
    task_name, prev_time_spent, completed = task

    hours, minutes = timer_length.split(':')
    timer_length_s = ((int(hours) * 60) + int(minutes)) * 60
    elapsed_s = 0

    while elapsed_s <= timer_length_s:
        cls()
        print(Colors.YELLOW + task_name + Colors.NORMAL + '\n')
        print('Timer Length: ' +
              Colors.GREEN + f"{timer_length}:00" + Colors.NORMAL)
        print('Elapsed Time: ' +
              f'{elapsed_s // 3600}:' +
              f'{(elapsed_s // 60):02}:' +
              f'{(elapsed_s % 60):02}' + '\n')
        print(Colors.WHITE +
              'Press `Ctrl + C` to stop the timer' +
              Colors.NORMAL + '\n')
        try:
            sleep(1)
            elapsed_s += 1
        except KeyboardInterrupt:
            break

    if elapsed_s >= timer_length_s:
        alarm(5)
        
    prev_hours, prev_minutes = prev_time_spent.split(':')
    prev_s = ((int(prev_hours) * 60) + int(prev_minutes)) * 60

    seconds = elapsed_s + prev_s
    hours, minutes = divmod(seconds // 60, 60)
    return task_name, f"{hours:01}:{minutes:02}", False


def alarm(repetitions: int):
    try:
        for repetition in range(repetitions):
            for alarm in range(5):
                print('\a', end='', flush=True)
                sleep(.1)
            sleep(1.5)
    except KeyboardInterrupt:
        pass
