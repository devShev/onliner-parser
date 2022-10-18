from typing import Optional

from pydantic import BaseModel

from onliner_parser.save_manager import SavingObject


class BasePrice(BaseModel):
    amount: Optional[float] = None


class MinPricesMedian(BasePrice):
    pass


class PriceMin(BasePrice):
    pass


class PriceMax(BasePrice):
    pass


class Sale(BaseModel):
    is_on_sale: Optional[bool] = None
    discount: Optional[int] = None
    min_prices_median: Optional[MinPricesMedian] = None


class Offers(BaseModel):
    count: Optional[int] = None


class Prices(BaseModel):
    price_min: Optional[PriceMin] = None
    price_max: Optional[PriceMax] = None
    offers: Optional[Offers] = None


class ProductReviews(BaseModel):
    rating: Optional[int] = None
    count: Optional[int] = None
    html_url: Optional[str] = None


class Page(BaseModel):
    limit: Optional[int] = None
    items: Optional[int] = None
    current: Optional[int] = None
    last: Optional[int] = None


class PriceHistoryLog(BaseModel):
    date: Optional[str] = None
    price: Optional[float] = None


class CharData(BaseModel):
    items: list[PriceHistoryLog]

    def get_items_tuple(self) -> tuple[tuple[str | None, float | None]]:
        items = []
        for item in self.items:
            data = item.date
            price = item.price
            items.append((data, price))

        return tuple(items)


class Product(BaseModel, SavingObject):
    id: Optional[int] = None
    key: Optional[str] = None
    full_name: Optional[str] = None
    name_prefix: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    html_url: Optional[str] = None
    reviews: Optional[ProductReviews] = None
    prices: Optional[Prices] = None
    sale: Optional[Sale] = None

    price_history: Optional[tuple[tuple[str | None, float | None]]] = None
    item_spec: Optional[dict] = None

    def to_dict(self) -> dict:
        dict_attrs = {
            'id': self.id,
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
    page: Optional[Page]
    total_ungrouped: int

    def get_products(self) -> list[Product]:
        return [
            product for product in self.products
            if product.status == 'active'
        ]

    def get_last_page(self) -> int:
        return self.page.last


class BasePriceHistoryJSONResponse(BaseModel):
    chart_data: Optional[CharData] = None

    def get_items(self) -> tuple[tuple[str | None, float | None]]:
        return self.chart_data.get_items_tuple()
