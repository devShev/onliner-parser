import os
import pandas as pd

from onliner_parser.models import Product
from onliner_parser.utils import Font
from onliner_parser.utils import DataTransformer


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

    def save(self, filename: str = 'products', save_format: str = 'csv') -> None:
        if self.__data:
            self.__create_directory()

            list_of_prods = [product.to_dict() for product in self.__data]
            df = pd.DataFrame(list_of_prods)

            data_transformer = DataTransformer()
            df = data_transformer.transform_dp_fields(df, self.__data)

            filepath = f'{self.__directory_name}{filename}.{save_format}'
            try:
                if save_format == 'csv':
                    df.to_csv(filepath)
                else:
                    df.to_excel(filepath, sheet_name='Products', na_rep='-')
            except BaseException as e:
                print(f'{Font.WARN} Recording error{Font.NORMAL}')
                print(f'{Font.ERROR} {e}')

            else:
                print(f'{Font.INFO} Data saved to {filename}.{save_format}{Font.NORMAL}')

        else:
            print(f'{Font.WARN} There is nothing to save{Font.NORMAL}')
