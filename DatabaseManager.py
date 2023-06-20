import os.path
import sqlite3
from datetime import datetime
from enum import Enum


class Status(Enum):
    TO_DO = "to do"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


class Task:
    def __init__(self, id_task, priority, title, description, creation_time, last_modification, status):
        self.id_task = id_task
        self.priority = priority
        self.title = title
        self.description = description
        self.creation_time = creation_time
        self.last_modification = last_modification
        self.status = status

    def __iter__(self):
        return iter((self.id_task, self.priority, self.title, self.description, self.creation_time,
                     self.last_modification, self.status))

    def get_task_info(self):
        return f"Task ID: {self.id_task}\nPriority: {self.priority}\nTitle: {self.title}\nDescription: {self.description}\nCreation Time: {self.creation_time}\nLast Modification: {self.last_modification}\nStatus: {self.status}"


log_path = "TaskManagerLog.txt"
db_path = "Tasks.db"

available_status_values = [status.value for status in Status]


def create_database():
    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        if not os.path.exists(log_path):
            open(log_path, "w")
        return con
    except sqlite3.Error as e:
        print("An error occurred while connecting to the database:", e)
        return None



def create_task_table_if_not_exists(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TASKS'")
        result = cur.fetchone()
        if result is None:
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS TASKS (
            IdTask INTEGER PRIMARY KEY ASC,
            Priority INTEGER NOT NULL,
            Title VARCHAR(100) NOT NULL,
            Description VARCHAR(255),
            CreatedAt DATETIME NOT NULL,
            LastModification DATETIME,
            Status VARCHAR(10) NOT NULL
            )""")
            con.commit()
            append_to_log(f"Task table created at {datetime.now()}\n")
    except sqlite3.Error as e:
        append_to_log(f"An error occurred while creating the tasks table: {e} - {datetime.now()}\n", True)


def get_task_list(con, status):
    cur = con.cursor()
    if status == "":
        cur.execute("SELECT * FROM Tasks")
    else:
        cur.execute("SELECT * FROM Tasks WHERE Status = ?", (status,))
    tasks = cur.fetchall()

    return [Task(task['IdTask'], task['Priority'], task['Title'], task['Description'], task['CreatedAt'],
                 task['LastModification'], task['Status']) for task in tasks]


def add_new_task(con, title, description):
    try:
        cur = con.cursor()
        cur.execute("SELECT COALESCE(MAX(IdTask), 0) FROM Tasks")
        max_id = cur.fetchone()[0]
        current_time = datetime.now()
        new_task = Task(max_id + 1, 5, title, description, current_time, current_time, Status.TO_DO.value)
        cur.execute("INSERT INTO Tasks (IdTask, Priority, Title, Description, CreatedAt, LastModification, Status) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?);", tuple(new_task))
        con.commit()
        append_to_log(f"New task added: Title={title}, Description={description}, CreatedAt={current_time}\n")
        print("Successfully added a new task.")
    except sqlite3.Error as e:
        append_to_log(f"An error occurred while adding a new task: {e}\n", True)


def delete_task(con, task_id):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Tasks WHERE IdTask = ?", (task_id,))
        result = cur.fetchone()

        if result is None:
            append_to_log(f"Task ID {task_id} does not exist\n", True)
            return
        task = Task(*result)
        cur.execute("DELETE FROM Tasks WHERE IdTask = ?", (task_id,))
        con.commit()
        append_to_log(f"Task deleted: ID={task.id_task}, Title='{task.title}', Description='{task.description}'\n",
                      True)
    except sqlite3.Error as e:
        append_to_log(f"An error occurred while deleting the task: {e}\n")


def edit_task(con, task_id):
    print("Edit Task:")
    print("Available parameters: 'title', 'description', 'status', 'priority'")
    print("Enter 'quit' to exit.")

    while True:
        user_answer = input("Enter a parameter: ").lower()

        if user_answer == "quit":
            break

        if user_answer not in ["title", "description", "status", "priority"]:
            print("Invalid input. Please try again.")
            continue

        if user_answer == "status":
            print(f"Available status values: {', '.join(available_status_values)}")

        if user_answer == "priority":
            print("Enter the new priority (1-10): ")

        new_value = input(f"Enter the new {user_answer}: ")

        if user_answer == "status" and new_value.lower() not in available_status_values:
            print("Invalid input. Please enter a valid status.")
            continue

        if user_answer == "priority" and (not new_value.isdigit() or int(new_value) < 1 or int(new_value) > 10):
            print("Invalid input. Priority must be a number between 1 and 10.")
            continue

        update_task(con, user_answer.capitalize(), task_id, new_value)


def update_task(con, parameter, task_id, new_value):
    try:
        cur = con.cursor()
        cur.execute(f"SELECT {parameter} FROM Tasks WHERE IdTask = ?", (task_id,))
        result = cur.fetchone()
        if result is None:
            print("Task ID does not exist.")
            return
        old_value = result[0]
        current_time = datetime.now()
        cur.execute(f"UPDATE Tasks SET {parameter} = ?, LastModification = ? WHERE IdTask = ?",
                    (new_value, current_time, task_id))
        con.commit()
        append_to_log(f"Task ID {task_id} - {parameter} updated: {old_value} -> {new_value} at {current_time}\n")
        print(f"Task {parameter} updated successfully.")
    except sqlite3.Error as e:
        append_to_log(f"An error occurred while updating the task {parameter}: {e}\n", True)


def find_task(con, parameter, value):
    try:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Tasks WHERE {parameter} = ?", (value,))
        tasks = cur.fetchall()
        return [Task(task['IdTask'], task['Priority'], task['Title'], task['Description'], task['CreatedAt'],
                     task['LastModification'], task['Status']) for task in tasks]
    except sqlite3.Error as e:
        print(f"An error occurred while selecting the task:", e)


def drop_table(con):
    try:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Tasks")
        con.commit()
        print("Table dropped successfully.")
        append_to_log(f"Table 'Tasks' dropped at {datetime.now()}\n")
    except sqlite3.Error as e:
        print("An error occurred while dropping the table:", str(e))


def append_to_log(log_message, print_message=False):
    with open(log_path, "a") as log_file:
        log_file.write(log_message)
    if print_message:
        print(log_message)
