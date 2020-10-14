# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

engine = create_engine('sqlite:///todo.db?check_same_thread=False') # Our DB file name
Base.metadata.create_all(engine) # Our DB
Session = sessionmaker(bind=engine) # To access ou DB

session = Session() # From here to close() we manipulate our DB

today = datetime.today()
todays_date = today.day
month = today.strftime('%b')

def read_table():
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"Today {todays_date} {month}:")
    if not rows:
        print("Nothing to do!\n")
    else:
        task_number = 1
        for task in rows:
            print(f"{task_number}. {task.task}")
            task_number += 1
        print()

def weeks_tasks():
    for i in range(7):
        day = today + timedelta(days=i)
        day_name = day.strftime("%A")
        day_of_month = day.day
        month = day.strftime('%b')
        print(f"{day_name} {day_of_month} {month}:")

        tasks = session.query(Table).filter(Table.deadline == day.date()).all()
        if not tasks:
            print("Nothing to do!\n")
        else:
            task_number = 1
            for task in tasks:
                print(f"{task_number}. {task.task}")
                task_number += 1
            print()

def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    number = 1
    for row in rows:
        print(f"{number}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        number += 1
    print()

def add_new_row():
    new_row = Table(task=input("Enter task\n"), deadline=datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d"))
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")

def missed_tasks():
    missed_tasks = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline)
    print("Missed tasks:")
    task_number = 1
    if not missed_tasks:
        print("Nothing is missed!\n")
    else:
        for missed in missed_tasks:
            print(f"{task_number}. {missed}. {missed.deadline.day} {missed.deadline.strftime('%b')}")
            task_number += 1
        print()

def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    number = 1
    print("Chose the number of the task you want to delete:")
    for row in rows:
        print(f"{number}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        number += 1
    useless_row = rows[int(input())-1]
    session.delete(useless_row)
    session.commit()
    print("The task has been deleted!\n")

while True:
    menu = input("1) Today's tasks\n" +
                 "2) Week's tasks\n" +
                 "3) All tasks\n" +
                 "4) Missed tasks\n" +
                 "5) Add task\n" +
                 "6) Delete task\n" +
                 "0) Exit\n")
    print()
    if menu == "1": # Read the table
        read_table()

    elif menu == "2": # Weeks tasks
        weeks_tasks()

    elif menu == "3": # All tasks
        all_tasks()

    elif menu == "4": # Missed tasks
        missed_tasks()

    elif menu == "5": # Add a new row
        add_new_row()

    elif menu == "6": #Delete task
        delete_task()

    elif menu == "0": # Exit
        break
print("Bye!")
session.close()