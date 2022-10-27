import pandas as pd
import numpy as np
import plotly.graph_objects as go


class DataProcManager:
    def __init__(self, file=None, ) -> None:
        self.file = file
        self.data = pd.read_csv(file)

    @staticmethod
    def __get_products_on_review_rate() -> list[int]:
        """
        Gets the best products on review rate
        Returns
        -------
        product_ids: list[int]

        """

        return [42342]

    @staticmethod
    def __get_products_on_price_review_rate() -> list[int]:
        """
        Gets the best products on price review rate
        Returns
        -------
        product_ids: list[int]

        """

        return [42342]

    @staticmethod
    def __get_shop_offers_on_price_review_rate() -> list[int]:
        """
        Gets the best shop offers on price review rate
        Returns
        -------
        shop_ids: list[int]

        """

        return [42342]

    @staticmethod
    def __get_roducts_price_history_plots() -> list[bytes]:
        """
        Gets the items price history plots
        Returns
        -------
        img_bytes: list[bytes]
        """
        np.random.seed(1)

        N = 100
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        sz = np.random.rand(N) * 30

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=go.scatter.Marker(
                size=sz,
                color=colors,
                opacity=0.6,
                colorscale="Viridis"
            )
        ))
        img_bytes = fig.to_image(format="png")
        return [img_bytes]
