from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
import pandas as pd


class StockPredictInterface(ABC):
    def __init__(self, data: list[tuple[dict, pd.DataFrame]], prediction_days: int):
        """

        :param data: list of combined data from stock receiver
        """

        self.historical_data = None
        self.thicker_info = None
        self.training_data_dict = None

        self.thicker_info_zip, self.historical_data_zip = None, None

        self.x_train: Optional[np.array] = None
        self.y_train: Optional[np.array] = None
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

    def prepare_data(self, data: list[tuple[dict, pd.DataFrame]]):
        self.thicker_info = [thicker_info for thicker_info, _ in data]
        self.historical_data = [historical_data for _, historical_data in data]
        self.thicker_info_zip, self.historical_data_zip = zip(*data)
        print("IS EQUAL: ", self.thicker_info == self.thicker_info_zip, self.historical_data == self.historical_data_zip)
        self.training_data_dict = {thicker_info["symbol"]: historical_data for thicker_info, historical_data in data}