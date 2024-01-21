from typing import Optional

import numpy as np
import pandas as pd

from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface
from sklearn.preprocessing import MinMaxScaler


class LstmStockPredict(StockPredictInterface):
    """This class will predict the stock market using LSTM neural network model. Prediction will base on Close price"""

    def __init__(self, data: tuple[dict, pd.DataFrame]):
        """
        :param data: data received from stock receiver
        """
        super().__init__(data)
        self.scaled_data: Optional[pd.DataFrame] = None
        self.__prediction_days = None  # handled in property
        # TODO change to np.ndarray
        self.x_train: list= []
        self.y_train: list = []

    def predict(self) -> float:
        """
        This function will predict if the stock market is ready to buy

        :return: tomorrow price prediction
        """
        self.__scale_data()

    def __scale_data(self):
        """
        This function will scale the data to be between 0 and 1

        :return: scaled data
        """
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = scaler.fit_transform(self.historical_data["Close"].values.reshape(-1, 1))

    def __prepare_train_data(self):
        """
        This function will prepare the data to be trained
        """
        # country = self.thicker_info.get("country", None)
        # if country is None:
        #     raise ValueError("Country is not defined")
        for x in range(self.prediction_days, len(self.scaled_data)):
            self.x_train.append(self.scaled_data[x - self.prediction_days:x, 0])
            self.y_train.append(self.scaled_data[x, 0])

    def fit(self):
        """
        This function will fit the data to the model
        """
        pass

    @property
    def prediction_days(self):
        if self.scaled_data:
            return len(self.scaled_data)
        raise ValueError("Scaled data is not defined")

    @prediction_days.setter
    def prediction_days(self, value):
        raise NotImplementedError("Prediction days cannot be set")