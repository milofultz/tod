# Today todo list

# DATA STRUCTURE
# Array of tuples:
#   (name: str, complete: bool)

# MAIN
# opening screen shows all todos and timebox
# > 'init' (new day), add, edit, complete, delete, clean up

# INIT
# clear all previous tasks (ALL)
# do loop of adding new tasks and their length
# when done, back to main

# ADD
# Add new task and timebox

# ADD + #
# option for insertion at certain order

# EDIT
# Change content of task n
# show current info
# if nothing entered, keep current
# when finished replace task n with 'new' edited task

# COMPLETE
# mark task n as complete

# DELETE
# remove task n from list

# CLEAN UP
# remove all completed tasks from list


# TRACK INTEGRATION
# track will read from the file
# if tasks exist, when starting main loop, ask if user wants to add
# accomplishments from tod file of date YYYYMMDD


def get_tasks():
    # open and read data from file
    # for all tasks in file
    #   parse number, description, and time
    #   put them in an array as tuples
    # return tasks
    pass

def add_task(tasks: list, new_task: str, timebox: str, index: int=-1):
    if index == -1:
        index = len(tasks)
    tasks.insert(index, (new_task, timebox, False))
    return tasks

def edit_task(tasks: list, index: int):
    # get user input
    #   task name (if none, use existing)
    #   task timebox (if none, use existing)
    # replace task at index with new task
    # return tasks
    pass

def complete_task(tasks: list, index: int):
    # add completed flag to task at index
    # return tasks
    pass

def delete_task(tasks: list, index: int):
    # remove task at index from list
    # return tasks
    pass

def clean_tasks(tasks: list):
    # for each task in list
    #   if it's completed, remove it
    #   if not, pass
    # return tasks
    pass