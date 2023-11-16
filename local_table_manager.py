import os

import pandas as pd


class PandasHandler:

    def __init__(self, file_name):

        self.file_name = file_name

        # Читаем данные, если файл существует
        if os.path.exists(file_name):
            self.df = pd.read_excel(file_name)
        else:
            self.df = pd.DataFrame()

    def write_row(self, data):


        # Добавляем новые колонки
        for col in data.keys():
            self.add_column(col)

        # Создаем DataFrame из данных
        row_df = pd.DataFrame([data])

        # Добавляем в общий DataFrame
        self.df = pd.concat([self.df, row_df]).reset_index(drop=True)

    def get_column_index(self, name):
        if name in self.df.columns:
            return self.df.columns.get_loc(name)
        else:
            return None

    def add_column(self, name):
        if name not in self.df.columns:
            self.df[name] = None

    def save(self):
        self.df.to_excel(self.file_name, index=False)

    def close(self):
        self.save()


# Использование
# table = PandasHandler('data.csv')
# data = {
#   'Название': 'iPhone 12',
#   'Цена': '60 000 р.',
#   'Скидка': '5%',
#     'новый столбец':'123'
# }
#
# table.write_row(data)