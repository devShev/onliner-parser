import csv
import os
from abc import ABC, abstractmethod

import pandas as pd

from onliner_parser.terminal_font_style import Font


class SavingObject(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """Преобразование объекта в словарь без вложенности"""

    @staticmethod
    @abstractmethod
    def get_fields() -> tuple:
        """Вернуть названия полей"""


class NotSavingObject(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'NotSavingObject, {self.message}'
        else:
            return f'NotSavingObject raised!'


class SaveManager:
    __data: list
    __directory_name: str = 'data/'
    __class: type[SavingObject]

    excel_formats: tuple = (
            'xlsx',
            'xlsm',
            'xlsb',
            'xlam',
            'xltx',
            'xltm',
            'xls',
            'xla',
            'xlt',
            'excel',
        )

    def __init__(self, cls: type[SavingObject], data: list) -> None:
        if issubclass(cls, SavingObject):
            self.__class = cls
        else:
            raise NotSavingObject('Передаваемый класс не наследует SavingObject')
        self.__data = data

    def __create_directory(self):
        if not os.path.exists(f'{self.__directory_name}'):
            os.makedirs(f'{self.__directory_name}')

    def set_directory_name(self, name: str) -> None:
        self.__directory_name = name

    def save(self, filename: str = 'products', save_format: str = 'csv'):
        if save_format in SaveManager.excel_formats:
            self.save_xlsx(filename)
        else:
            self.save_csv(filename)

    def save_xlsx(self, filename: str = 'products') -> None:
        if self.__data:
            self.__create_directory()
            data = [product.to_dict() for product in self.__data]

            df = pd.DataFrame(data)

            filepath = f'{self.__directory_name}{filename}.xlsx'
            try:
                df.to_excel(filepath, sheet_name='Products', na_rep='-')

            except BaseException as e:
                print(f'{Font.WARN} Ошибка записи{Font.NORMAL}')
                print(f'{Font.ERROR} {e}')

            else:
                print(f'{Font.INFO} Данные сохранены в {filename}.xlsx{Font.NORMAL}')

        else:
            print(f'{Font.WARN} Нечего сохранять{Font.NORMAL}')

    def save_csv(self, filename: str = 'products') -> None:
        if self.__data:
            self.__create_directory()
            filepath = f'{self.__directory_name}{filename}.csv'

            try:
                with open(filepath, mode='w', encoding='utf-8') as file:
                    fields = self.__class.get_fields()

                    writer = csv.DictWriter(
                        file,
                        delimiter=',',
                        lineterminator="\r",
                        fieldnames=fields,
                    )

                    writer.writeheader()
                    for product in self.__data:
                        writer.writerow(product.to_dict())

            except BaseException as e:
                print(f'{Font.WARN} Ошибка записи{Font.NORMAL}')
                print(f'{Font.ERROR} {e}')
            else:
                print(f'{Font.INFO} Данные сохранены в {filename}.csv{Font.NORMAL}')

        else:
            print(f'{Font.WARN} Нечего сохранять{Font.NORMAL}')
