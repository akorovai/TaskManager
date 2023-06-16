import sys

from DatabaseManager import *

con = create_database()
if con is None:
    sys.exit()

create_task_table_if_not_exists(con)

print("TaskManager: " + datetime.now().strftime("%H:%M:%S %Y-%m-%d"))

while True:
    print("--- MENU ---")
    print("Task Database Commands: add, show, find, edit, delete, drop")
    print("Log Commands: log_show, log_clear")
    print("General Commands: quit")
    user_answer = input("Enter a command: ").lower()

    if user_answer in ["add", "show", "find", "edit", "delete", "drop"]:
        if user_answer == "add":
            add_new_task(con,
                         input("Enter the task title: "),
                         input("Enter the task description: "))
        elif user_answer == "show":
            sort_answer = input("Do you want to sort the tasks by LastModification? (yes/no): ")
            tasks = get_task_list(con,
                                  input("Enter the status to filter by (leave blank for all tasks): "))
            if len(tasks) != 0:
                sorted_tasks = sorted(tasks, key=lambda x: x.last_modification,
                                      reverse=True) if sort_answer.lower() == "yes" else tasks
                print("--- Sorted Tasks ---" if sort_answer.lower() == "yes" else "--- All Tasks ---")
                print("\n".join([task.get_task_info() for task in sorted_tasks]))
            else:
                print("Tasks list is empty!")
        elif user_answer == "find":
            tasks = find_task(con,
                              input("Choose parameter to find (title/decision): "),
                              input("Enter the value: "))
            if len(tasks) != 0:
                print("--- Matching Tasks ---")
                print("\n".join([task.get_task_info() for task in tasks]))
            else:
                print("No matching tasks found!")
        elif user_answer == "edit":
            tasks = get_task_list(con, "")
            if len(tasks) != 0:
                print("--- All Tasks ---")
                print("\n".join([task.get_task_info() for task in tasks]))
                task_id = input("Enter the ID of the task to edit: ")
                if task_id.isdigit():
                    edit_task(con, int(task_id))
                else:
                    print("Invalid task ID. Please enter a valid task ID.")
            else:
                print("Tasks list is empty!")
        elif user_answer == "delete":
            tasks = get_task_list(con, "")
            if len(tasks) != 0:
                print("--- All Tasks ---")
                print("\n".join([task.get_task_info() for task in tasks]))
                task_id = input("Enter the ID of the task to delete: ")
                if task_id.isdigit():
                    delete_task(con, int(task_id))
                else:
                    print("Invalid task ID. Please enter a valid task ID.")
            else:
                print("Tasks list is empty!")
        elif user_answer == "drop":
            print("Dropping task table...")
            drop_table(con)
            break

    elif user_answer in ["log_show", "log_clear"]:
        if user_answer == "log_show":
            print("--- Log ---")
            log_file_path = "TaskManagerLog.txt"
            if os.path.exists(log_file_path):
                if os.path.getsize(log_file_path) > 0:
                    with open(log_file_path, "r") as log_file:
                        print(log_file.read())
                else:
                    print("Log is Empty!")
            else:
                print("Log file does not exist.")
        elif user_answer == "log_clear":
            confirmation = input("Are you sure you want to clear the log file? (yes/no): ")
            if confirmation.lower() == "yes":
                log_file_path = "TaskManagerLog.txt"
                if os.path.exists(log_file_path):
                    with open(log_file_path, "w") as log_file:
                        log_file.write("")
                    print("Log file cleared successfully.")
                else:
                    print("Log file does not exist.")
            else:
                print("Log clearance canceled.")

    elif user_answer == "quit":
        print("Exiting the application...")
        break

    else:
        print("Invalid command. Please try again.")
