from typing import Optional

from pydantic import BaseModel

from onliner_parser.save_manager import SavingObject


class BasePrice(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None


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


class Product(SavingObject, BaseModel):
    id: Optional[int] = None
    key: Optional[str] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    name_prefix: Optional[str] = None
    extended_name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    micro_description: Optional[str] = None
    html_url: Optional[str] = None
    reviews: Optional[ProductReviews] = None
    prices: Optional[Prices] = None
    sale: Optional[Sale] = None

    def to_dict(self) -> dict:
        dict_attrs = {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'full_name': self.full_name,
            'name_prefix': self.name_prefix,
            'extended_name': self.extended_name,
            'status': self.status,
            'description': self.description,
            'micro_description': self.micro_description,
            'html_url': self.html_url,
            'reviews_rating': self.reviews.rating,
            'reviews_html_url': self.reviews.html_url,
            'reviews_count': self.reviews.count,
            'sale_is_on_sale': self.sale.is_on_sale,
            'sale_discount': self.sale.discount,
            'sale_min_prices_median_amount': self.sale.min_prices_median.amount,
            'sale_min_prices_median_currency': self.sale.min_prices_median.currency,
        }
        if self.prices:
            dict_attrs.update(
                {
                    'prices_price_min_amount': self.prices.price_min.amount,
                    'prices_price_min_currency': self.prices.price_min.currency,
                    'prices_price_max_amount': self.prices.price_max.amount,
                    'prices_price_max_currency': self.prices.price_max.currency,
                    'prices_offers_count': self.prices.offers.count,
                }
            )

        return dict_attrs

    @staticmethod
    def get_fields():
        return (
            'id',
            'key',
            'name',
            'full_name',
            'name_prefix',
            'extended_name',
            'status',
            'description',
            'micro_description',
            'html_url',
            'reviews_rating',
            'reviews_html_url',
            'reviews_count',
            'prices_price_min_amount',
            'prices_price_min_currency',
            'prices_price_max_amount',
            'prices_price_max_currency',
            'prices_offers_count',
            'sale_is_on_sale',
            'sale_discount',
            'sale_min_prices_median_amount',
            'sale_min_prices_median_currency',
        )


class BaseJSONResponse(BaseModel):
    products: list[Product]
    total: int
    page: Optional[Page]
    total_ungrouped: int

    def get_products(self) -> list[Product]:
        return self.products

    def get_last_page(self) -> int:
        return self.page.last
