import time
from random import uniform

import bs4
from progress.bar import IncrementalBar
from requests import Session, Response
from requests.exceptions import ConnectionError

from onliner_parser.models import (BaseJSONResponse,
                                   BasePriceHistoryJSONResponse, Product)
from onliner_parser.utils import Font


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
    __items_count: int
    __current_item_index: int = 0

    def __init__(self, url: str) -> None:
        category = url.split('/')[-1] + '?group=1'
        self.__url += category

    def __del__(self) -> None:
        self.__session.close()

    @staticmethod
    def __random_wait(start: float = 0.1, finish: float = 0.3) -> None:
        """Random waiting in the specified range"""
        sec = uniform(start, finish)
        time.sleep(sec)

    def __get_response(self, url: str = None) -> Response:
        """Get response from Site"""
        response: Response
        while True:
            try:
                if url:
                    response = self.__session.get(url)
                else:
                    response = self.__session.get(self.__url, headers=self.__headers, params=self.__params)
            except ConnectionError:
                self.__random_wait(1, 2)
            else:
                if response.status_code == 200:
                    return response
                else:
                    self.__random_wait()

    def __set_base_json_response(self, json: str) -> None:
        """
        Set BaseJSONResponse
        json: str - json response
        """
        self.__base_json_response = BaseJSONResponse.parse_raw(json)

    def __set_last_page(self, page: int) -> None:
        """
        Set last page for parse
        page: int - page number
        """
        self.__last_page = page

    def __extend_data(self, data: list[Product]) -> None:
        """Adding new data to memory"""
        self.__data.extend(data)

    def __inc_current_page(self) -> bool:
        """Increasing the current parsing page until it is equal to the last page"""
        self.__params['page'] = self.__params.get("page") + 1
        if self.__params['page'] <= self.__last_page:
            return True
        return False

    def __inc_current_item_index(self) -> bool:
        """Increasing current item index until it is equal items count"""
        if self.__current_item_index < self.get_items_count() - 1:  # -1 because list start from 0
            self.__current_item_index += 1
            return True
        return False

    def __get_price_history(self, key: str) -> tuple:
        url = f'https://catalog.api.onliner.by/products/{key}/prices-history?period=6m'

        response = self.__get_response(url)

        base_price_history_json_response = BasePriceHistoryJSONResponse().parse_raw(response.text)
        return base_price_history_json_response.get_items()

    def __get_item_spec(self, url: str) -> dict:
        response = self.__get_response(url)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        [bad_div.decompose() for bad_div in soup.find_all('div', class_='product-tip-wrapper')]
        tbodys = soup.select('table[class="product-specs__table"] tbody')
        specs = dict()
        for tbody in tbodys:
            tr_list = tbody.find_all('tr')
            title = tr_list[0].text.strip()
            info = dict()
            for tr in tr_list[1:]:
                names = [" ".join(tag.text.split()) for tag in tr.select('td') if tag.text]
                descs = [" ".join(tag.text.split()) for tag in tr.select('td span[class="value__text"]')]
                dict_ = dict(zip(names, descs))
                info.update(dict_)
            specs.update({title: info})
        return specs

    def __deep_parse_item(self, item: Product) -> None:
        item.price_history = self.__get_price_history(item.key)
        item.item_spec = self.__get_item_spec(item.html_url)

    def __parse(self) -> None:
        """Parsing process"""
        start = time.time()

        response: Response = self.__get_response()

        self.__set_base_json_response(response.text)
        self.__set_last_page(self.__base_json_response.get_last_page())

        print(f'{Font.INFO} Starting parsing....')

        self.__extend_data(self.__base_json_response.get_products())
        # Show progress
        bar = IncrementalBar(f'{Font.YELLOW}Parsing process:{Font.NORMAL}', max=self.__last_page)
        bar.next()

        while self.__inc_current_page():
            response = self.__get_response()
            self.__set_base_json_response(response.text)
            self.__extend_data(self.__base_json_response.get_products())
            bar.next()
            self.__random_wait()

        print()  # Empty line for normal output
        finish = time.time()
        executing_time = time.strftime("%H:%M:%S", time.gmtime(round(finish - start, 2)))
        print(f'{Font.INFO} Parsing completed! Execution time: {executing_time}{Font.NORMAL}')

        self.__items_count = len(self.__data)

    def __parse_next(self) -> bool:
        """Parse next item in data"""
        if not self.__data:
            self.__parse()

        current_index = self.__current_item_index
        self.__deep_parse_item(self.__data[current_index])

        return self.__inc_current_item_index()

    def __deep_parse(self) -> None:
        """Deep parsing process"""
        if not self.__data:
            self.__parse()

        start = time.time()
        print(f'{Font.INFO} Starting deep parsing...')
        bar = IncrementalBar(f'{Font.YELLOW}Deep parsing process:{Font.NORMAL}', max=len(self.__data))

        for item in self.__data:
            self.__deep_parse_item(item)
            bar.next()
            self.__random_wait()

        print()  # Empty line for normal output

        finish = time.time()
        executing_time = time.strftime("%H:%M:%S", time.gmtime(round(finish - start, 2)))
        print(f'{Font.INFO} Deep parsing completed! Execution time: {executing_time}{Font.NORMAL}')

    def parse(self) -> None:
        """Start parsing"""
        self.__parse()

    def deep_parse(self) -> None:
        """Start deep parsing"""
        return self.__deep_parse()

    def parse_next(self) -> bool:
        """Parse next item in data"""
        return self.__parse_next()

    def get_data(self) -> list[Product]:
        """Returns the parsed data"""
        if self.__data:
            return self.__data
        print(f'{Font.ERROR} Nothing to return')

    def insert_data(self, data: list[Product]) -> None:
        """Insert data into parser"""
        if not self.__data:
            self.__data = data
        else:
            print(f'{Font.ERROR} The parser already contains data')

    def get_items_count(self) -> int:
        """Return count of items"""
        if self.__items_count:
            return self.__items_count
        print(f'{Font.ERROR} Nothing to return')
