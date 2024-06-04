""" .py file with result of task 1.
    Task:
    Разработать метод, на вход которого подается PDF файл (сам файл предоставляется во вложении). 
    Нужно прочитать всю возможную информацию из файла и на выходе вернуть в виде словаря.
    
    * При оценке решения будут учитываться как покрытие, так и архитектурные решения 
    (по возможности – подумайте о потенциальном масштабировании)
"""

import os
import glob
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def parse_pdf(path: str) -> dict:
    """ Return dictionary with content of all pdf files in the foler.
        Input parameter - path - is a path where target files are placed.
    """

    # Check existing path.
    if not os.path.exists(path):
        raise ValueError('Path not found')

    file_list = list(glob.glob("*.pdf"))
    result_dict = {}

    # Cycle for each file in target folder.
    for pdf_file in file_list:

        file_dict = {}
        # Cycle for each page in file.
        for page_num, page_content in enumerate(extract_pages(pdf_file)):
            page_dict = {}
            element_num = 0

            # Flag for field "NOTE" - next field is a NOTE content.
            notes_flag = False
            for element in page_content:
                if isinstance(element, LTTextContainer):

                    parsed_text = element.get_text().split(':')
                    label = parsed_text[0].removesuffix('\n').removesuffix(' ')

                    if label == '':
                        continue

                    if element_num == 0:
                        # The highest element - is a title without key.
                        label = 'Title'
                        value = parsed_text[0]
                    elif len(parsed_text) == 2:
                        value = parsed_text[1]
                    else:
                        value = ''

                    if label == 'NOTES':
                        notes_flag = True
                        continue

                    if notes_flag:
                        value = label
                        label = 'NOTES'
                        notes_flag = False

                    page_dict[label] = value.removesuffix('\n').removesuffix(' ').removeprefix(' ')

                element_num += 1
            file_dict[page_num] = page_dict
        result_dict[pdf_file] = file_dict

    return result_dict
