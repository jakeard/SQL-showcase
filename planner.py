import sqlite3 as sql
import time

# create DB
connect = sql.connect('planner.db')
cursor = connect.cursor()

# create tables in DB
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY, task TEXT UNIQUE, time REAL, year TEXT, month TEXT, day TEXT, type_id INTEGER, FOREIGN KEY(type_id) REFERENCES types(type_id))")
cursor.execute("CREATE TABLE IF NOT EXISTS types (type_id INTEGER PRIMARY KEY, type TEXT UNIQUE)")

# insert types into the types table
cursor.execute('SELECT * FROM types')
if len(cursor.fetchall()) == 0:
    count = 0
    while count != 5:
        count += 1
        if count == 1:
            values = (None, 'Chores')
        elif count == 2:
            values = (None, 'Homework')
        elif count == 3:
            values = (None, 'Work')
        elif count == 4:
            values = (None, 'Exercise')
        elif count == 5:
            values = (None, 'Other')
        cursor.execute("INSERT INTO types VALUES (?, ?)", values)
        connect.commit()

def get_choice(max, phrase, do_phrase=True):
    # gets the user's choice for the given amount of numbers
    choice = 0
    while choice > max or choice < 1:
        try:
            if do_phrase:
                print(phrase)
            choice = int(input('-> '))
            print()
            if choice > max or choice < 1:
                print('Not a valid number.')
                time.sleep(.5)
        except ValueError:
            print('\nNot a valid number.')
            time.sleep(.5)
    return choice

def get_all():
    # returns all of the data needed to show all tasks and their types, due dates, and times
    cursor.execute("SELECT ta.task, ty.type, (ta.month || '/' || ta.day || '/' || ta.year) AS date, ta.time FROM tasks ta JOIN types ty ON ta.type_id = ty.type_id ORDER BY ta.year, ta.month, ta.day, ta.time")
    return cursor.fetchall()

def get_tasks():
    # returns only the task names
    cursor.execute("SELECT task FROM tasks")
    return cursor.fetchall()

def get_types():
    # returns only the type names
    cursor.execute("SELECT * FROM types")
    return cursor.fetchall()

def get_value(data, new=False):
    # get's the value for the given variable (time or date)
    value = -1
    while value < 0:
        try:
            if data == 'hours':
                # get the amount of hours
                value = float(input('\nTime to complete in hours: '))
            elif data == 'type':
                while value > 5 or value < 1:
                    if not new:
                        value = int(input('\nType ID: '))
                    else:
                        value = int(input('\nNew type ID: '))
                    if value > 5 or value < 1:
                        print('\nNot a valid number.')
                        time.sleep(.5)
            else:
                date = []
                correct = False
                cursor.execute("SELECT strftime('%Y', date('now'))")
                current_date = cursor.fetchall()
                for i in current_date:
                    for j in i:
                        now_year = j   
                while not correct:
                    # get the year the task is due
                    year = input('\nDue date year (yyyy): ')
                    if len(year) != 4 or int(year) < 0 or year < now_year:
                        print('\nNot a valid number.')
                        time.sleep(.5)
                    else:
                        correct = True
                        date.append(year)
                correct = False
                while not correct:
                    caught = False
                    cursor.execute("SELECT strftime('%m', date('now'))")
                    current_date = cursor.fetchall()
                    for i in current_date:
                        for j in i:
                            now_month = j
                    # get the month the task is due
                    month = input('\nDue date month (mm): ')
                    try:
                        int(month)
                    except:
                        caught = True
                    if caught or len(month) != 2 or int(month) > 12 or int(month) < 1 or (month < now_month \
                        and year == now_year):
                        print('\nNot a valid number.')
                        time.sleep(.5)
                    else:
                        correct = True
                        date.append(month)
                correct = False
                cursor.execute("SELECT strftime('%d', date('now'))")
                current_date = cursor.fetchall()
                for i in current_date:
                    for j in i:
                        now_day = j   
                while not correct:
                    # get the day the task is due
                    day = input('\nDue date day (dd): ')
                    try:
                        int(day)
                    except:
                        caught = True
                    # error checking and test to see if leap year for correct amount of days if month is february
                    if caught or (int(day) < 1) or len(day) != 2 or (int(month) in {1, 3, 5, 7, 8, 10, 12} \
                        and int(day) > 31) or (int(month) in {4, 6, 9, 11} and int(day) > 30) or (month == \
                            '02' and (int(year) % 400 == 0 or int(year) % 4 == 0 and int(year) % 100 != 0) \
                                and int(day) > 29) or (month == '02' and (int(year) % 400 != 0 and int(year) \
                                    % 100 == 0 or int(year) % 4 != 0) and int(day) > 28) or (day < now_day \
                                        and month == now_month and year == now_year): 
                        print('\nNot a valid number.')
                        time.sleep(.5)
                    else:
                        correct = True
                        date.append(day)
                # if trying to get date value, return date list of year, month, day
                return date
            if value < 0:
                print('\nNot a valid number.')
                time.sleep(.5)
        except ValueError:
            print('\nNot a valid number.')
            time.sleep(.5)
            value = -1
    # if trying to get time value, return time value
    return value 

def display_tasks():
    # displays the stored tasks created by the user from the DB
    tasks = get_all()
    print('\n{:<20}  {:<20}  {:<20}  {:<20}'.format('Task', 'Type', 'Due', 'Time'))
    print('{:<20}  {:<20}  {:<20}  {:<20}'.format('-----', '-----', '----', '-----'))
    for task in tasks:
        print('{:<20}  {:<20}  {:<20}  {:<1} {:<1}'.format(task[0], task[1], task[2], task[3], 'hours'))

def display_types():
    # displays all the types of tasks
    types = get_types()
    print('\n{:<15}  {:<15}'.format('Type ID', 'Type'))
    print('{:<15}  {:<15}'.format('--------', '-----'))
    for type in types:
        print('{:<15}  {:<15}'.format(type[0], type[1]))

# begin main
print('Welcome to your planner!')

choice = None
while choice != 3:
    # beginning user input choice
    choice = get_choice(3, '\nWhat would you like to do?\n1). View Tasks\n2). Edit Planner\n3). Quit')
    
    if choice == 1:
        # to view the tasks
        display_tasks()


    elif choice == 2:
        # gives them the choice of what they want to edit
        choice = get_choice(5, '\nWould you like to:\n1). Add\n2). Edit\n3). Delete\n4). Reset planner\n5). Go back')

        if choice == 1:
            # if user wants to add a task, get task, type, date, and time and insert into the DB
            passed = False
            while not passed:
                bad = False
                task = input('Task: ')
                tasks = get_tasks()
                for i in tasks:
                    for j in i:
                        if task == j:
                            print('\nTask already exists.\n')
                            time.sleep(.5)
                            bad = True
                            break
                    if bad:
                        break
                if not bad:
                    passed = True
            display_types()
            type_id = get_value('type')
            hours = get_value('hours')
            date = get_value('date')
            values = (None, task, hours, date[0], date[1], date[2], type_id)
            cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", values)
            connect.commit()

        elif choice == 2:
            # if user wants to edit a task, ask which task
            display_tasks()
            tasks = get_tasks()
            bad = True
            while bad:
                print('\nWhich task would you like to edit?')
                edit = input('-> ')
                for i in tasks:
                    for j in i:
                        if edit == j:
                            bad = False
                            break
                    if not bad:
                        break
                if bad:
                    print('\nNot a valid task.')
                    time.sleep(.5)
            # ask what they want to change from the task they chose
            choice = get_choice(4, '\nWould you like to edit:\n1). Task\n2). Type\n3). Due date\n4). Time')
            if choice == 1:
                # update the task name
                task = input('Task: ')
                values = (task, edit)
                cursor.execute("UPDATE tasks SET task = ? WHERE task = ?", values)
            elif choice == 2:
                # update the type
                display_types()
                type_id = get_value('type', True)
                values = (type_id, edit)
                cursor.execute("UPDATE tasks SET type_id = ? WHERE task = ?", values)
            elif choice == 3:
                # update the due date
                choice = None
                date = get_value('date')
                values = (date[0], date[1], date[2], edit)
                cursor.execute("UPDATE tasks SET year = ?, month = ?, day = ? WHERE task = ?", values)
            elif choice == 4:
                # update the time
                hours = get_value('hours')
                values = (hours, edit)
                cursor.execute("UPDATE tasks SET time = ? WHERE task = ?", values)
            connect.commit()

        elif choice == 3:
            # if user wants to delete a task, ask which task
            choice = 0
            display_tasks()
            print('\nWhich task would you like to delete?')
            choice = input('-> ')
            values = (choice,)
            cursor.execute("DELETE FROM tasks WHERE task = ?", values)
            connect.commit()
            
        elif choice == 4:
            # if user wants to reset the planner entirely, make sure and then delete everything from the DB
            verify = input('\nAre you sure you want to reset the planner (y/n)? ').lower()
            if verify == 'y':
                cursor.execute('DELETE FROM tasks')
            else:
                pass