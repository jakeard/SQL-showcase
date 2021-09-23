import sqlite3 as sql
import time

connect = sql.connect('planner.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY, task TEXT, type TEXT, time REAL)")

def get_choice(max, phrase, do_phrase=True):
    choice = 0
    while choice > max or choice < 1:
        try:
            if do_phrase:
                print(phrase)
            choice = int(input('-> '))
            if choice > max or choice < 1:
                print('\nNot a valid number.')
                time.sleep(.5)
            if choice <= max and choice > 0:
                return choice
        except ValueError:
            print('\nNot a valid number.')
            time.sleep(.5)

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

def display_tasks(tasks, numbers=True):
    if numbers:
        print('\n{:<5}  {:<15}  {:<15}  {:<15}'.format('ID', 'Task', 'Type', 'Time'))
        print('{:<5}  {:<15}  {:<15}  {:<15}'.format('---', '-----', '-----', '-----'))
        for task in tasks:
            print('{:<5}  {:<15}  {:<15}  {:<15}'.format(task[0] + 1, task[1], task[2], task[3]))
    else:
        print('\n{:<15}  {:<15}  {:<15}'.format('Task', 'Type', 'Time'))
        print('{:<15}  {:<15}  {:<15}'.format('-----', '-----', '-----'))
        for task in tasks:
            print('{:<15}  {:<15}  {:<15}'.format(task[1], task[2], task[3]))

print('Welcome to your planner!')

choice = None
while choice != 3:
    # Get the choice number to know what to do: view the tasks, edit the tasks, or end the program
    choice = get_choice(3, '\nWhat would you like to do?\n1). View Tasks\n2). Edit Planner\n3). Quit')
    
    if choice == 1:
        #if user chooses choice 1, display all tasks, the task type, and the task time
        tasks = get_tasks()
        display_tasks(tasks, False)

    if choice == 2:
        # if user choose choice 2, display the choices for editing and allow for answer
        choice = get_choice(5, '\nWould you like to:\n1). Add\n2). Edit\n3). Delete\n4). Reset planner\n5). Go back')
        if choice == 1:
            # if choice is 1 (add a new task) ask for the task name, what type of task it is, and how long it will take
            task = input('\nTask: ')
            type = input('Type of task: ')
            hours = -1
            while hours < 0:
                try:
                    hours = float(input('Time to complete in hours: '))
                except ValueError:
                    print('\nNot a valid number.\n')
                    time.sleep(.5)
            tasks = get_tasks()
            values = (len(tasks), task, type, hours)
            cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?)", values) #insert the ID, and the inputs from the user to the database
            connect.commit()
        elif choice == 2:
            tasks = get_tasks()
            display_tasks(tasks)
            choice = get_choice(len(tasks), '\nWhich number task would you like to edit? ')
            task_id = choice - 1
            choice = get_choice(3, '\nWould you like to edit:\n1). Task\n2). Type\n3). Time')

            if choice == 1:
                task = input('\nTask: ')
                values = (task, task_id)
                cursor.execute("UPDATE tasks SET task = ? WHERE task_id = ?", values)
                connect.commit()
            elif choice == 2:
                type = input('\nType of task: ')
                values = (type, task_id)
                cursor.execute("UPDATE tasks SET type = ? WHERE task_id = ?", values)
                connect.commit()
            elif choice == 3:
                choice = None
                hours = -1
                while hours < 0:
                    try:
                        hours = float(input('\nTime to complete in hours: '))
                        if hours < 0:
                            print('\nNot a valid number.')
                            time.sleep(.5)
                    except ValueError:
                        print('\nNot a valid number.')
                        time.sleep(.5)
                        hours = -1
                values = (hours, task_id)
                cursor.execute("UPDATE tasks SET time = ? WHERE task_id = ?", values)
                connect.commit()
                


        elif choice == 3:
            tasks = get_tasks()
            choice = 0
            while choice < 1 or choice > len(tasks):
                display_tasks(tasks)
                choice = get_choice(len(tasks), '\nWhich number task would you like to delete?')
            task_id = choice - 1
            values = (task_id,)
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", values)
            connect.commit()
            tasks = get_tasks()
            for task in tasks:
                if task[0] > task_id: 
                    values = (task[0] - 1, task_id)
                    cursor.execute("UPDATE tasks SET task_id = ? WHERE task_id = ?", values)
                    connect.commit()
            choice = None
            



        elif choice == 4:
            verify = input('\nAre you sure you want to reset the planner (y/n)? ')
        elif choice == 5:
            pass
        else:
            pass

        

    
    