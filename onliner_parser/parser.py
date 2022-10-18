from time import sleep
from random import uniform
import time

from requests import Session
from progress.bar import IncrementalBar

from onliner_parser.models import BaseJSONResponse, Product
from onliner_parser.terminal_font_style import Font


class CatalogParser:
    __session: Session = Session()

    __url: str = 'https://catalog.onliner.by/sdapi/catalog.api/search/'
    __headers: dict = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'application/json, text/javascript, */*; q=0.01',
    }
    __params: dict = {
        'page': 1,
    }

    __base_json_response: BaseJSONResponse
    __data: list[Product] = []
    __last_page: int

    def __init__(self, url: str) -> None:
        category = url.split('/')[-1]
        self.__url += category

    def __del__(self) -> None:
        self.__session.close()

    def __get_json_response(self) -> str:
        """Получение ответа"""
        return self.__session.get(self.__url, headers=self.__headers, params=self.__params).text

    def __set_base_json_response(self, json: str) -> None:
        """
        Назначение объекта json ответа
        json: str - json строка ответа
        """
        self.__base_json_response = BaseJSONResponse.parse_raw(json)

    def __set_last_page(self, page: int) -> None:
        """
        Установка последней страницы для парсинга
        page: int - последняя страница
        """
        self.__last_page = page

    def __extend_data(self, data: list[Product]) -> None:
        """Добавление новых данных в память"""
        self.__data.extend(data)

    def __increment_current_page(self) -> bool:
        """Увеличение текущей страницы парсинга до тех пор, пока она не будет равна последней странице"""
        self.__params['page'] = self.__params.get("page") + 1
        if self.__params['page'] <= self.__last_page:
            return True
        return False

    @staticmethod
    def __random_wait(start: float, finish: float) -> None:
        """Случайное ожидание в указанном диапазоне"""
        sec = uniform(start, finish)
        sleep(sec)

    def __parse(self) -> None:
        """Запуск парсинга"""
        start = time.time()

        self.__set_base_json_response(self.__get_json_response())
        self.__set_last_page(self.__base_json_response.get_last_page())

        print(f'{Font.INFO} Начало парсинга...')

        self.__extend_data(self.__base_json_response.get_products())
        # Отображение состояния парсинга
        bar = IncrementalBar(f'{Font.YELLOW}Процесс парсинга:{Font.NORMAL}', max=self.__last_page)
        bar.next()

        while self.__increment_current_page():
            self.__set_base_json_response(self.__get_json_response())
            self.__extend_data(self.__base_json_response.get_products())
            bar.next()
            self.__random_wait(0.1, 0.3)

        print()  # Empty line for normal output
        finish = time.time()
        executing_time = round(finish - start, 2)
        print(f'{Font.INFO} Парсинг завершён! Время выполнения {executing_time} сек. {Font.NORMAL}')

    def parse(self) -> None:
        """Запуск парсинга"""
        self.__parse()

    def get_data(self) -> list[Product]:
        """Отдаёт полученные данные"""
        if self.__data:
            return self.__data
        print(f'{Font.WARN} Нечего возвращать')
