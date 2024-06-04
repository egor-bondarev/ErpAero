"""

    У вас есть таблица в которой вы передаете свои значение (переменная table) и ответ из вебсокета бэкенда
    
    Вам нужно написать механизм который будет принимать таблицу (table) и преобразовать её в запрос json 

    Так же мы знаем что ключи из таблицы = значениям в base_ws , так же учитывать что ключи в table могут находится в разном порядке 

    Как результат вы должны собрать то что в переменной result
    файл - additional_task.py
    * При оценке решения будут учитываться сбор , гибкость и устойчивость к ошибкам
"""
import re
import json
import dataclasses
from Task_3.structures import Result, ColorCondition, Column, Condition, OrderBy

def table_to_json(table: list[dict[str, str]], websocket_response: dict, base_ws: dict) -> str:
    """ Inpit parameters:
        table - our input table,
        websocket_response - data with accordance between columns and the index with the filter.
        base_ws - column names for output.
    """

    def add_list_to_dict(target_dict: dict, key: str, input_list: list) -> dict:
        if target_dict is None:
            colors = {}
            colors[key] = input_list
            target_dict = colors
        else:
            target_dict[key] = input_list
        return target_dict

    result = Result(columns=[])
    dictionary_counter = 0

    # Cycle for each column from table.
    for dictionary in table:

        # Variables for column characteristics.
        column_view = ''
        web_socket_index = ''
        web_socket_filter = ''

        # Cycle for each value in column.
        for key in dictionary:
            value = dictionary[key]
            base_value = base_ws[key]
            if value == '':
                continue

            match base_value:
                case 'columns':
                    # Filling column's characteristics.
                    column_view = dictionary[key]
                    web_socket_index = websocket_response[column_view]['index']
                    web_socket_filter = websocket_response[column_view]['filter']

                    column = Column(index=web_socket_index, sort=dictionary_counter)
                    result.columns.append(column)

                case 'order_by':
                    order_by = OrderBy(direction=value, index=web_socket_index)
                    result.order_by = order_by

                case 'conditions_data':
                    value_list = value.partition(',')
                    condition_list = []

                    # Cycle for each value in the sequence.
                    for item in value_list:
                        if item in [',', '']:
                            continue

                        type_value = item.partition('=')
                        condition = Condition(type=type_value[0], value=type_value[2])
                        condition_list.append(condition)

                    result.conditions_data = add_list_to_dict(
                        result.conditions_data,
                        web_socket_filter,
                        condition_list)

                case 'color_conditions':
                    value_list = re.findall(
                        r'equals=[SP]\d+(?:=rgba\(\d{1,3},\d{1,3},\d{1,3},{1,3})?', value)
                    color_list = []

                    # Cycle for each value in the sequence.
                    for item in value_list:
                        values = str(item).split('=')
                        color = ColorCondition(type=values[0], value=values[1])

                        if len(values) == 3:
                            color.color = values[2]
                        color_list.append(color)

                        result.color_conditions = add_list_to_dict(
                            result.color_conditions,
                            web_socket_filter,
                            color_list)

                case 'page_size':
                    result.page_size = value

                case 'row_height':
                    result.row_height = value

        dictionary_counter += 1

    return json.dumps(dataclasses.asdict(result))
