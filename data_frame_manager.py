import os

import pandas as pd


class DataFrameManager:
    """Класс для формирования dataframe"""
    def __init__(self):
        self.df = pd.DataFrame()
        self.slice_count = 0
        self.step = 3 # количество строк в "пачке"
        self.number_characteristics = 3 # количество характеристик, которые идут в финальную таблицу

    def write_row(self, data, google_table):
        #ограничение google-таблицы
        data=dict(list(data.items())[:self.number_characteristics])

        # Добавляем новые колонки
        for col in data.keys():
            self.add_column(col)

        # Создаем DataFrame из данных
        row_df = pd.DataFrame([data])

        # Добавляем в общий DataFrame
        self.df = pd.concat([self.df, row_df]).reset_index(drop=True)
        self.df = self.df.fillna('')
        self.slice_count += 1

        #записываем в google-таблицу новую "пачку" строк
        if self.slice_count % self.step == 0:
            google_table.write_dataframe(self.df.iloc[self.slice_count - self.step:])

    def add_column(self, name):
        if name not in self.df.columns:
            self.df[name] = None

