import asyncio
import time
from random import uniform

import bs4
from aiohttp import ClientSession
from progress.bar import IncrementalBar
from requests import Response, Session
from requests.exceptions import ConnectionError

from onliner_parser.models import (BaseJSONResponse,
                                   BasePriceHistoryJSONResponse, Product)
from onliner_parser.utils import Font, Settings, exec_time


class CatalogParser:
    __session: Session = Session()
    SETTINGS: Settings = Settings()

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
        self.SETTINGS.deep_parse_status = True
        return False

    @staticmethod
    def __bs_parse(html: str) -> dict:
        soup = bs4.BeautifulSoup(html, 'html.parser')
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

    def __get_price_history(self, key: str) -> tuple:
        url = f'https://catalog.api.onliner.by/products/{key}/prices-history?period=6m'

        response = self.__get_response(url)

        base_price_history_json_response = BasePriceHistoryJSONResponse().parse_raw(response.text)
        return base_price_history_json_response.get_items()

    def __get_item_spec(self, url: str) -> dict:
        """Parse item spec by bs4"""
        response = self.__get_response(url)

        return self.__bs_parse(response.text)

    def __deep_parse_item(self, item: Product) -> None:
        """Deep parsing given item"""
        if self.SETTINGS.parse_history:
            item.price_history = self.__get_price_history(item.key)
        if self.SETTINGS.parse_spec:
            item.item_spec = self.__get_item_spec(item.html_url)

    async def __get_async_response(self, async_session: ClientSession, page: int):
        async with async_session.get(self.__url, params={'page': page}) as response:
            json = await response.text()
            bjr: BaseJSONResponse = BaseJSONResponse.parse_raw(json)
            self.__extend_data(bjr.get_products())

    async def __get_future_instance(self):
        tasks = []
        async with ClientSession() as async_session:
            for page in range(1, self.__last_page + 1):
                task = asyncio.ensure_future(self.__get_async_response(async_session, page=page))
                tasks.append(task)

            await asyncio.gather(*tasks)

    async def __async_deep_parse_item(self, async_session: ClientSession, item: Product):
        if self.SETTINGS.parse_spec:
            async with async_session.get(item.html_url) as response:
                html = await response.text()
                item.item_spec = self.__bs_parse(html)
        if self.SETTINGS.parse_history:
            url = f'https://catalog.api.onliner.by/products/{item.key}/prices-history?period=6m'
            async with async_session.get(url) as response:
                json = await response.text()
                base_price_history: BasePriceHistoryJSONResponse = BasePriceHistoryJSONResponse().parse_raw(json)
                item.price_history = base_price_history.get_items()

    async def __get_future_instance_deep_parse(self):
        tasks = []
        async with ClientSession() as async_session:
            for prod in self.__data:
                task = asyncio.ensure_future(self.__async_deep_parse_item(async_session, prod))
                tasks.append(task)

            await asyncio.gather(*tasks)

    @exec_time()
    def __async_parse(self) -> None:
        """Async parsing process"""
        response: Response = self.__get_response()

        self.__set_base_json_response(response.text)
        self.__set_last_page(self.__base_json_response.get_last_page())

        self.__extend_data(self.__base_json_response.get_products())

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.__get_future_instance())
        loop.run_until_complete(future)

        self.__items_count = len(self.__data)

    @exec_time(start_text='Start deep parsing...', end_text='Deep parsing completed!')
    def __async_deep_parse(self) -> None:
        """Async deep parsing"""
        if not self.__data:
            self.__async_parse()

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.__get_future_instance_deep_parse())
        loop.run_until_complete(future)

        self.SETTINGS.deep_parse_status = True

    @exec_time()
    def __parse(self) -> None:
        """Parsing process"""
        response: Response = self.__get_response()

        self.__set_base_json_response(response.text)
        self.__set_last_page(self.__base_json_response.get_last_page())

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

        self.__items_count = len(self.__data)

    def __parse_next(self) -> bool:
        """Parse next item in data"""
        if not self.__data:
            self.__parse()

        current_index = self.__current_item_index
        self.__deep_parse_item(self.__data[current_index])

        return self.__inc_current_item_index()

    @exec_time(start_text='Start deep parsing...', end_text='Deep parsing completed!')
    def __deep_parse(self) -> None:
        """Deep parsing process"""
        if not self.__data:
            self.__parse()

        bar = IncrementalBar(f'{Font.YELLOW}Deep parsing process:{Font.NORMAL}', max=len(self.__data))

        for item in self.__data:
            self.__deep_parse_item(item)
            bar.next()
            self.__random_wait()

        self.SETTINGS.deep_parse_status = True

    def parse(self) -> None:
        """Start parsing"""
        self.__parse()

    def async_parse(self) -> None:
        """Start async parsing"""
        self.__async_parse()

    def deep_parse(self) -> None:
        """Start deep parsing"""
        self.__deep_parse()

    def async_deep_parse(self) -> None:
        """Start async deep parse"""
        self.__async_deep_parse()

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
