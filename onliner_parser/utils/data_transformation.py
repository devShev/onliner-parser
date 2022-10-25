import pandas as pd
import time
from onliner_parser.models import Product


class DataTransformer:
    @staticmethod
    def __get_price_history_df(products_data: list[Product]) -> pd.DataFrame:
        """
        Transform initial tuple[tuple[str, float]] structure to dataframe str - float
        Parameters
        ----------
        products_data: list[Product]

        Returns
        -------
        desc_df: pd.Dataframe()
            df with month - price columns

        """
        p_h_data: list[list] = []
        columns = [tuple_[0] + "_price" for tuple_ in products_data[0].price_history[:-1]]
        columns.insert(0, "id")
        for product in products_data:
            price_history = list(map(list, product.price_history[:-1]))

            price_history = [list_[1] for list_ in price_history]
            price_history.insert(0, product.id)

            p_h_data.append(price_history)
        return pd.DataFrame(p_h_data, columns=columns)

    @staticmethod
    def __get_specification_df(products_data: list[Product]) -> pd.DataFrame:
        """
        Transform initial dict[str, [dict[str,str] | str]] structure to dataframe of strs
        Parameters
        ----------
        products_data: list[Product]

        Returns
        -------
        desc_df: pd.Dataframe()
            df with columns that descript product

        """
        desc_df = pd.DataFrame()
        for prod in products_data:
            df_ = pd.DataFrame.from_dict({j: prod.item_spec[i][j]
                                          for i in prod.item_spec.keys()
                                          for j in prod.item_spec[i].keys()},
                                         orient="index")
            df_ = df_.transpose()
            df_["id"] = prod.id
            desc_df = pd.concat([desc_df, df_])
        desc_df.reset_index(inplace=True)
        return desc_df

    def transform_dp_fields(self, full_df: pd.DataFrame(), products_data: list[Product], settings) -> pd.DataFrame():
        """
        Transform deep parsed fields
        Parameters
        ----------
        full_df: pd.DataFrame()
        products_data: list[Product]
        settings: Settings
            class of bool vars(parse or not)

        Returns
        -------
        full_df: pd.Dataframe()
            transfromed df

        """
        full_df.drop(["price_history", "item_spec"], axis=1, inplace=True)

        # transform fields from deep parsing
        if settings.parse_history:
            p_h_df = self.__get_price_history_df(products_data)
            full_df = full_df.merge(p_h_df, on="id")
        if settings.parse_spec:
            spec_df = self.__get_specification_df(products_data)
            full_df = full_df.merge(spec_df, on="id")
        return full_df
