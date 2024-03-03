from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class StockPredictInterface(ABC):
    def __init__(self, data: tuple[dict, pd.DataFrame], prediction_days: int):
        """

        :param data: data from stock receiver
        """
        self.thicker_info, self.historical_data = data
        self.scaled_data = None
        self.prediction_days = prediction_days

    @abstractmethod
    def predict(self) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :param data: data frame with Close, Volume, Dividends, Stock Splits, Country

        :return: tomorrow price prediction
        """
        pass
