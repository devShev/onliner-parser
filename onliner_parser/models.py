from typing import Optional

from pydantic import BaseModel


class BasePrice(BaseModel):
    amount: float = None


class MinPricesMedian(BasePrice):
    pass


class PriceMin(BasePrice):
    pass


class PriceMax(BasePrice):
    pass


class Sale(BaseModel):
    is_on_sale: bool = None
    discount: int = None
    min_prices_median: MinPricesMedian = None


class Offers(BaseModel):
    count: int = None


class Prices(BaseModel):
    price_min: PriceMin = None
    price_max: PriceMax = None
    offers: Offers = None


class ProductReviews(BaseModel):
    rating: int = None
    count: int = None
    html_url: str = None


class Page(BaseModel):
    limit: int = None
    items: int = None
    current: int = None
    last: int = None


class PriceHistoryLog(BaseModel):
    date: Optional[str] = None
    price: Optional[float] = None


class ChartData(BaseModel):
    items: list[PriceHistoryLog]

    def get_items_tuple(self) -> tuple:
        items = []
        for item in self.items:
            data = item.date
            price = item.price
            items.append((data, price))

        return tuple(items)


class Product(BaseModel):
    id: int = None
    key: str = None
    full_name: str = None
    name_prefix: str = None
    status: str = None
    description: str = None
    html_url: str = None
    reviews: ProductReviews = None
    prices: Prices = None
    sale: Sale = None

    price_history: tuple = None
    item_spec: dict = None

    def to_dict(self) -> dict:
        dict_attrs = {
            'id': self.id,
            'key': self.key,
            'full_name': self.full_name,
            'name_prefix': self.name_prefix,
            'description': self.description,
            'html_url': self.html_url,
            'reviews_rating': self.reviews.rating,
            'reviews_html_url': self.reviews.html_url,
            'reviews_count': self.reviews.count,
            'sale_is_on_sale': self.sale.is_on_sale,
            'sale_discount': self.sale.discount,
            'sale_min_prices_median_amount': self.sale.min_prices_median.amount,
            'item_spec': self.item_spec,
        }
        if self.prices:
            dict_attrs.update(
                {
                    'prices_price_min_amount': self.prices.price_min.amount,
                    'prices_price_max_amount': self.prices.price_max.amount,
                    'prices_offers_count': self.prices.offers.count,
                    'price_history': self.price_history,
                }
            )

        return dict_attrs

    @staticmethod
    def get_fields():
        return (
            'id',
            'key',
            'full_name',
            'name_prefix',
            'description',
            'html_url',
            'reviews_rating',
            'reviews_html_url',
            'reviews_count',
            'prices_price_min_amount',
            'prices_price_max_amount',
            'prices_offers_count',
            'sale_is_on_sale',
            'sale_discount',
            'sale_min_prices_median_amount',
            'price_history',
            'item_spec',
        )


class BaseJSONResponse(BaseModel):
    products: list[Product]
    total: int
    page: Page
    total_ungrouped: int

    def get_products(self) -> list[Product]:
        return [
            product for product in self.products
            if product.status == 'active'
        ]

    def get_last_page(self) -> int:
        return self.page.last


class BasePriceHistoryJSONResponse(BaseModel):
    chart_data: ChartData = None

    def get_items(self) -> tuple:
        return self.chart_data.get_items_tuple()
