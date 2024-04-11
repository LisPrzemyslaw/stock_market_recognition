from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class StockPredictInterface(ABC):
    def __init__(self, data: tuple[dict, pd.DataFrame], prediction_days: int):
        """

        :param data: data from stock receiver
        :param name: name of the stock to save the data
        """
        self.thicker_info, self.historical_data = data
        self.scaled_data = None
        self.prediction_days = prediction_days
        self.name = self.thicker_info["symbol"].lower()

    @abstractmethod
    def predict(self, last_days_close_values: np.array) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :param last_days_close_values: last days close values

        :return: tomorrow price prediction
        """
        pass

    @abstractmethod
    def fit(self) -> None:
        """
        This function will fit the data to the model
        """
        pass
