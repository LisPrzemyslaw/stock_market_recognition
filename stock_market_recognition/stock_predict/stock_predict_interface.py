from abc import ABC, abstractmethod

import pandas as pd


class StockPredictInterface(ABC):
    def __init__(self, data: tuple[dict, pd.DataFrame]):
        """

        :param data: data from stock receiver
        """
        self.thicker_info, self.historical_data = data

    @abstractmethod
    def predict(self) -> str:
        """
        This function will predict if the stock market is ready to buy

        :param data: data frame with Close, Volume, Dividends, Stock Splits, Country

        :return: string "BUY", "SELL", or "WAIT"
        """
        pass


class Prediction:
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"
