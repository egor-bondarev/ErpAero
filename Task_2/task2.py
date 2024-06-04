"""
    Используя этот файл как эталон для последующих проверок, разработать механизм, 
    проверяющий другие входящие pdf-файлы (как тестируемые) на соответствие структуры эталона.
    
    * При оценке решения будут учитываться тесты на: расположение на листе
    и наличие всех необходимых элементов, структуру текста, данные баркодов.
"""
from dataclasses import dataclass
from functools import total_ordering
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

@total_ordering
@dataclass
class ElementData:
    element_name: str
    x: int
    y: int

    def __eq__(self, element):
        return self.x == element.x

    def __gt__(self, element):
        return self.x > element.x

def compare_files(etalon_file_path: str, testing_file_path: str):
    """ Compare two pdf files. """

    etalon_struct = get_pdf_structure(etalon_file_path)
    test_struct = get_pdf_structure(testing_file_path)

    etalon_num = len(etalon_struct)
    test_num = len(test_struct)
    assert etalon_num == test_num, f'Fileds count in file: {test_num}, but expected: {etalon_num}'

    for item_num, item in enumerate(etalon_struct):

        etalon_field_name = item.element_name
        test_field_name = test_struct[item_num].element_name
        assert etalon_field_name == test_field_name, \
            f'Field name has value {test_field_name}, but expected {etalon_field_name}.'

        etalon_field_x = item.x
        test_field_x = test_struct[item_num].x
        assert etalon_field_x == test_field_x, \
            f'Field {etalon_field_name} has x coordintate value {etalon_field_x}, '\
                f'but expected {test_field_x}.'

        etalon_field_y = item.y
        test_field_y = test_struct[item_num].y
        assert etalon_field_y == test_field_y, \
            f'Field {etalon_field_name} has x coordintate value {etalon_field_y}, '\
                f'but expected {test_field_y}.'

def get_pdf_structure(pdf_file) -> list[ElementData]:
    """ Method for creation file structure with fields and coordinates, based on input file. """
    result_struct= []

    # Cycle for each page in the file.
    for _, page_content in enumerate(extract_pages(pdf_file)):
        element_num = 0
        notes_flag = False

        for element in page_content:
            if isinstance(element, LTTextContainer):
                parsed_text = element.get_text().partition(':')
                if element_num == 0:
                    element_name = 'Title'
                else:
                    element_name = parsed_text[0].removesuffix('\n').removesuffix(' ')

                if element_name == '':
                    continue

                # For Note field content save the left top coordinate.
                if notes_flag:
                    element_name = 'NOTES CONTENT'
                    notes_flag= False
                    y_coordinate = element.y1
                else:
                    y_coordinate = element.y0

                if element_name == 'NOTES':
                    notes_flag = True

                element_data = ElementData(
                    element_name=element_name,
                    x=int(element.x0),
                    y=int(y_coordinate)
                )
                result_struct.append(element_data)
            element_num += 1
    result_struct.sort()
    return result_struct
