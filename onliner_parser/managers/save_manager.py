import csv
import os

import pandas as pd

from onliner_parser.models import Product
from onliner_parser.utils import Font


class SaveManager:
    __data: list[Product]
    __directory_name: str = 'data/'

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

    def __init__(self, data: list[Product]) -> None:
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
                    fields = Product.get_fields()

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
