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
        self.ticker_info = None
        self.training_data_dict = None

        self.thicker_info_zip, self.historical_data_zip = None, None

        self.x_train_historical_data: Optional[np.array] = None
        self.x_train_stock_ticker: Optional[np.array] = None
        self.y_train: Optional[np.array] = None

        self.scaled_data = None
        self.prediction_days = prediction_days

        self.prepare_data(data)

    @abstractmethod
    def predict(self, ticker_symbol: str, last_days_close_values: np.array) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :param ticker_symbol: stock ticker symbol
        :param last_days_close_values: last days close values

        :return: tomorrow price prediction
        """
        pass

    @abstractmethod
    def fit(self):
        pass

    def prepare_data(self, data: list[tuple[dict, pd.DataFrame]]):
        """
        This function will prepare the data to be trained

        :param data: list of combined data from stock receiver

        :return:
        """
        self.ticker_info = [ticker_info for ticker_info, _ in data]
        self.historical_data = [historical_data for _, historical_data in data]
        self.thicker_info_zip, self.historical_data_zip = zip(*data)
        print("IS EQUAL: ", self.ticker_info == self.thicker_info_zip, self.historical_data == self.historical_data_zip)
        self.training_data_dict = {thicker_info["symbol"]: historical_data for thicker_info, historical_data in data}
