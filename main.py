import time

from config import table_id_input, table_id_output
from parser_page import PageParser
from table_manager import GoogleSheet
from data_frame_manager import DataFrameManager
from random import randint


def main():
    parser = PageParser()
    table_input = GoogleSheet('gs_credentials.json', table_id_input)
    table_output_google = GoogleSheet('gs_credentials.json', table_id_output, clear_list=True)
    table_output_local = DataFrameManager()

    for j in range(0, 5):
        list_links = table_input.get_links_for_processing(column_number=1, status_number=2)
        if len(list_links) == 0:
            break

        for i in list_links:
            try:
                pass
                dict_characteristics = parser.parse_characteristics(i[0])
                time.sleep(randint(1, 3))
                if dict_characteristics:
                    table_input.change_status_link(i[1])
                    table_output_local.write_row(dict_characteristics, table_output_google)
                time.sleep(randint(3, 6))
            except:
                print(f'ошибка обработки ссылки №{i[1]}')


if __name__ == '__main__':
    main()