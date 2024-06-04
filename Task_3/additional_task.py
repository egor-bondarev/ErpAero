

table = [{'Columns View': 'SO Number', 'Sort By': '', 'Highlight By': 'equals=S110=rgba(172,86,86,1),equals=S111', 'Condition': 'equals=S110,equals=S111', 'Row Height': '60', 'Lines per page': '25'},
         {'Columns View': 'Client PO', 'Sort By': '', 'Highlight By': 'equals=P110,equals=P111', 'Condition': 'equals=P110', 'Row Height': '', 'Lines per page': ''},
         {'Columns View': 'Terms of Sale', 'Sort By': 'asc', 'Highlight By': 'equals=S110=rgba(172,86,86,1)', 'Condition': '', 'Row Height': '', 'Lines per page': ''}]

websocket_response = {'Client PO': {'index': 'so_list_client_po', 'filter': 'client_po'},
                      'SO Number': {'index': 'so_list_so_number', 'filter': 'so_no'},
                      'Terms of Sale': {'index': 'so_list_terms_of_sale', 'filter': 'term_sale'}}

base_ws = {'Columns View': 'columns',
           'Sort By': 'order_by',
           'Condition': 'conditions_data',
           'Lines per page': 'page_size',
           'Row Height': 'row_height',
           'Highlight By': 'color_conditions'}
           
           
           
           

result = {'columns': [{'index': 'so_list_so_number', 'sort': 0}, 
                      {'index': 'so_list_client_po', 'sort': 1}, 
                      {'index': 'so_list_terms_of_sale', 'sort': 2}], 
          'order_by': {'direction': 'asc', 'index': 'so_list_terms_of_sale'},
          'conditions_data': {'so_no': [{'type': 'equals', 'value': 'S110'}, 
                                        {'type': 'equals', 'value': 'S111'}], 
                              'client_po': [{'type': 'equals', 'value': 'P110'}]}, 
          'page_size': '25', 
          'row_height': '60',
          'color_conditions': {'so_no': [{'type': 'equals', 'value': 'S110', 'color': 'rgba(172,86,86,1)'}], 
                               'client_po': [{'type': 'equals', 'value': 'S110', 'color': ''}, {'type': 'equals', 'value': 'S111', 'color': ''}],
                               'term_sale': []}, 
          'module': 'SO'}