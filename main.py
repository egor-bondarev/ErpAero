""" Main file for running any task method. """
from Task_1 import task1
from Task_2 import task2
from Task_3 import task3, additional_task as data

# Method for task1
task1_result = task1.parse_pdf('./')
print(task1_result)

print()

# Method for task2
task2.compare_files('./test_task.pdf', './test_task.pdf')
print()

# Method for task3
task3_result = task3.table_to_json(data.table, data.websocket_response, data.base_ws)
print(task3_result)
