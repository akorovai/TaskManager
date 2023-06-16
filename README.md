# Task Manager

This is a simple command-line task manager application written in Python.

## Description

The Task Manager allows you to perform various operations on tasks, such as adding, editing, deleting, and searching for tasks. It uses a SQLite database to store task information.

## Functionality

The Task Manager application provides the following functionality:

- **Add Task**: Add a new task with a title and description.
- **Show Tasks**: Display a list of all tasks, with the option to sort them by last modification.
- **Find Tasks**: Search for tasks based on their title or decision.
- **Edit Task**: Modify an existing task by updating its title, description, status, or priority.
- **Delete Task**: Remove a task from the database.
- **Drop Table**: Delete the entire task table from the database.
- **Show Log**: Display the contents of the log file.
- **Clear Log**: Clear the log file.
- **Quit**: Exit the application.

## Methods

The Task Manager application includes the following methods:

- `create_database()`: Create a connection to the SQLite database.
- `create_task_table_if_not_exists(con)`: Create the task table if it doesn't already exist.
- `get_task_list(con, status)`: Retrieve a list of tasks from the database, filtered by status.
- `add_new_task(con, title, description)`: Add a new task to the database.
- `delete_task(con, task_id)`: Delete a task from the database.
- `edit_task(con, task_id)`: Modify an existing task.
- `update_task(con, parameter, task_id, new_value)`: Update a specific parameter of a task.
- `find_task(con, parameter, value)`: Search for tasks based on a specific parameter and its value.
- `drop_table(con)`: Drop the task table from the database.
- `append_to_log(log_message, print_message=False)`: Append a log message to the log file.

## Getting Started

To run the Task Manager application, follow these steps:

1. Install Python.
2. Clone the repository: `git clone https://github.com/akorovai/TaskManager.git`
3. Open a terminal and navigate to the project directory: `cd TaskManager`
4. Run the application: `python main.py`

## Dependencies

The Task Manager application has the following dependencies:

- Python 3.x
- SQLite3

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
