from abc import ABC, abstractmethod

import pandas as pd


class StockReceiverInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def receive_data(self, stock_ticker: str) -> tuple[dict, pd.DataFrame]:
        """
        This method is returning data from the stock

        :param stock_ticker: name of stock ticker to receive

        :return: data frame with Close, Volume, Dividends, Stock Splits, Country
        """
        pass
