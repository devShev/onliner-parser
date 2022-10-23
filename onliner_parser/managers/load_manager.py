import csv

from onliner_parser.models import (MinPricesMedian, Offers, PriceMax, PriceMin,
                                   Prices, Product, ProductReviews, Sale)


# NOT SUPPORTED AT THIS TIME!!! DON'T USE THIS MANAGER!!!


class LoadManager:
    __data: list[Product] = []
    __directory_name: str = 'data/'

    def load_csv(self, filename: str = 'products') -> None:
        filepath = f'{self.__directory_name}{filename}.csv'

        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                reviews_rating = int(row.pop('reviews_rating'))
                reviews_html_url = str(row.pop('reviews_html_url'))
                reviews_count = int(row.pop('reviews_count'))
                reviews = ProductReviews(rating=reviews_rating, count=reviews_count, html_url=reviews_html_url)

                prices_price_min_amount = row.pop('prices_price_min_amount')
                prices_price_max_amount = row.pop('prices_price_max_amount')
                price_min = PriceMin(amount=float(prices_price_min_amount) if prices_price_min_amount else None)
                price_max = PriceMax(amount=float(prices_price_max_amount) if prices_price_max_amount else None)
                prices_offers_count = row.pop('prices_offers_count')
                offers = Offers(count=int(prices_offers_count) if prices_offers_count else None)
                prices = Prices(price_min=price_min, price_max=price_max, offers=offers)

                is_on_sale = True if row.pop('sale_is_on_sale') == "True" else False
                discount = int(row.pop('sale_discount'))
                min_prices_median = MinPricesMedian(amount=float(row.pop('sale_min_prices_median_amount')))
                sale = Sale(is_on_sale=is_on_sale, discount=discount, min_prices_median=min_prices_median)

                price_history = str(row.pop('price_history'))

                item_spec = str(row.pop('item_spec'))

                product = Product.parse_obj(row)
                product.reviews = reviews
                product.prices = prices
                product.sale = sale
                product.price_history = price_history
                product.item_spec = item_spec

                self.__data.append(product)

    def get_data(self) -> list[Product]:
        return self.__data
