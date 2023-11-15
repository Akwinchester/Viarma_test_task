import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:

    def __init__(self, credentials_file, spreadsheet_key):
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open_by_key(spreadsheet_key).sheet1

    def get_data(self, column_number):
        """Возвращает данные указанного столбца"""
        column = self.sheet.col_values(column_number)
        return column

    def write_data(self, row_number, column_number, value):
        """Записывает данные в указанную ячейку"""
        self.sheet.update_cell(row_number, column_number, value)

    def add_column(self, header):
        """Добавляет новый столбец с заголовком"""
        num_cols = len(self.sheet.row_values(1)) + 1
        self.sheet.update_cell(1, num_cols, header)

    def find_column(self, header):
        """Возвращает номер столбца по заголовку"""
        try:
            col = self.sheet.find(header).col
            return col
        except gspread.CellNotFound:
            return None

# table = GoogleSheet('credentials.json', '123456')
# links = table.get_data(1)
# table.write_data(2, 3, 'Some data')


# Подсоединение к Google Таблицам
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

# sheet = client.create("Yandex_parser")
# sheet.share('arsenijkiselev03@gmail.com', perm_type='user', role='writer')
