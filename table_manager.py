import gspread
from oauth2client.service_account import ServiceAccountCredentials
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class GoogleSheet:
    """Класс для работы с Google Sheets"""

    def __init__(self, credentials_file, spreadsheet_key, clear_list=False):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']

        # Авторизация и создание клиента
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, self.scope)
        self.client = gspread.authorize(self.creds)

        # Открываем таблицу и получаем лист
        self.spreadsheet = self.client.open_by_key(spreadsheet_key)
        self.worksheet = self.spreadsheet.get_worksheet(0)

        if clear_list:
            self.worksheet.clear()



    def get_links_for_processing(self, column_number, status_number):
        """
        Возвращает данные указанного столбца
        только для строк где в столбце B значение равно 0
        """

        values = self.worksheet.col_values(column_number)
        status = self.worksheet.col_values(status_number)

        filtered = []
        for i, val in enumerate(values):
            if str(status[i]) == '0':
                filtered.append((val, i+1)) #i - номер строки

        return filtered

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


    def write_dataframe(self, df):
        """Запись DataFrame в таблицу начиная с ячейки start_cell"""

        # Получаем заголовки колонок
        headers = list(df.columns)
        for h in headers:
            self.add_column(h)

        # Получаем значения DataFrame как список списков
        values = df.values.tolist()

        start_cell = 'A' + str(len(self.worksheet.get_all_values()) + 1)

        # Запись значений
        self.worksheet.update(start_cell, values, value_input_option='USER_ENTERED')

    def get_data(self):
        return self.worksheet.get_all_values()
