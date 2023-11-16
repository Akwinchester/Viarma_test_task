import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import table_id_input, table_id_output
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class GoogleSheet:
    """Класс для работы с Google Sheets"""

    def __init__(self, credentials_file, spreadsheet_key):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']

        # Авторизация и создание клиента
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, self.scope)
        self.client = gspread.authorize(self.creds)

        # Открываем таблицу и получаем лист
        self.spreadsheet = self.client.open_by_key(spreadsheet_key)
        self.worksheet = self.spreadsheet.get_worksheet(0)

    def get_data_column(self, column_number):
        """Возвращает данные указанного столбца"""
        column = self.worksheet.col_values(column_number)
        return column

    def get_links_for_processing(self, column_number):
        """
        Возвращает данные указанного столбца
        только для строк где в столбце B значение равно 1
        """

        values = self.worksheet.col_values(column_number)

        filtered = []
        for i, val in enumerate(values):
            if str(self.worksheet.cell(i + 1, 2).value) == '0':
                filtered.append(val)

        return filtered

    def write_data(self, row_number, column_number, value):
        """Записывает данные в указанную ячейку"""
        self.worksheet.update_cell(row_number, column_number, value)

    def change_status_link(self, row_number):
        """Помечает ссылку, как обработанную"""
        self.worksheet.update_cell(row_number, 2, 1)

    def add_column(self, header):
        """
        Добавляет новый столбец с заголовком
        если такого заголовка еще нет в таблице
        """

        # Получаем список существующих заголовков
        existing_headers = self.worksheet.row_values(1)

        # Проверяем, есть ли уже такой заголовок
        if header not in existing_headers:

            # Подсчитываем новый номер столбца
            num_cols = len(existing_headers) + 1

            # Добавляем новый заголовок
            self.worksheet.update_cell(1, num_cols, header)


    def find_column(self, header):
        """Возвращает номер столбца по заголовку"""
        try:
            col = self.worksheet.find(header).col
            return col
        except gspread.CellNotFound:
            return None

    def write_row(self, data):
        """
        Записывает словарь как строку в таблицу.
        Ключ - название столбца, значение - значение в ячейке.
        """

        # Получаем максимальный номер строки
        row = self.worksheet.row_count + 1

        # Добавляем новые столбцы для отсутствующих заголовков
        for header in data.keys():
            self.add_column(header)

        # Записываем данные в строку
        for header, value in data.items():
            col = self.find_column(header)
            self.worksheet.update_cell(row, col, value)


# Использование
table = GoogleSheet('gs_credentials.json', table_id_output)
data = {
  'Название': 'iPhone 12',
  'Цена': '65 000 р.',
  'Скидка': '5%'
}

table.write_row(data)



# # Подсоединение к Google Таблицам
# scope = ['https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive"]
#
# credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
# client = gspread.authorize(credentials)
#
# sheet = client.create("Yandex_parser_output")
# sheet.share('arsenijkiselev03@gmail.com', perm_type='user', role='writer')
