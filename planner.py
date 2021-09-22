import sqlite3 as sql

connect = sql.connect('planner.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tasks (type TEXT, task TEXT, time REAL)")

print('Welcome to your planner!')

choice = None
while choice != 3:
    print('\nWhat would you like to do?')
    print('1). View Tasks')
    print('2). Edit Planner')
    print('3). Quit')
    try:
        choice = int(input('-> '))
    except ValueError:
        print('\nNot a valid number.')
    
    if choice == 1:
        cursor.execute("SELECT * FROM tasks")
        print('\n{:<15}  {:<15}  {:<15}'.format('Type', 'Task', 'Time'))

        for task in cursor.fetchall():
            print('{:<15}  {:<15}  {:<15}\n'.format(task[0], task[1], task[2]))

    if choice == 2:
        print('\nWould you like to:')
        print('1). Add')
        print('2). Edit')
        print('3). Delete')
        print('4). Reset')
        print('5). Go back')
        try:
            choice = int(input('-> '))
        except ValueError:
            print('\nNot a valid number.')

        if choice == 1:
            task = input('\nTask: ')
            type = input('Type of task: ')
            time = float(input('Time to complete in hours: '))
            values = (type, task, time)
            cursor.execute("INSERT INTO tasks VALUES (?, ?, ?)", values)
            connect.commit()

        elif choice == 2:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            print('\nWhich number task would you like to edit? ')
            for i, task in enumerate(tasks):
                print(f'{i + 1}. {task[1]}')
            choice = int(input('-> '))
            task_name =tasks[choice - 1][1]
            print('\nWould you like to edit:')
            print('1). Task')
            print('2). Type')
            print('3). Time')
            try:
                choice = int(input('-> '))
            except ValueError:
                print('\nNot a valid number.')
            if choice == 1:
                task = input('\nTask: ')
                values = (task, task_name)
                cursor.execute("UPDATE tasks SET task = ? WHERE task = ?", values)
                connect.commit()
            elif choice == 2:
                type = input('Type of task: ')
                values = (type, task_name)
                cursor.execute("UPDATE tasks SET type = ? WHERE task = ?", values)
                connect.commit()
            elif choice == 3:
                choice = None
                time = float(input('Time to complete in hours: '))
                values = (time, task_name)
                cursor.execute("UPDATE tasks SET time = ? WHERE task = ?", values)
                connect.commit()
            else:
                print('Not a valid number.')
            




        elif choice == 3:
            delete = int(input('\nWhich number item would you like to delete? '))
            choice = None
        elif choice == 4:
            verify = input('\nAre you sure you want to reset the planner? (y/n) ')
        elif choice == 5:
            pass
        else:
            print('Not a valid number.')

        

    
    