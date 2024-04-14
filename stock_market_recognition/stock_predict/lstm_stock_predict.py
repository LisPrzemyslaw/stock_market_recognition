import os
from typing import Optional

import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout

from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface
from sklearn.preprocessing import MinMaxScaler


class LstmStockPredict(StockPredictInterface):
    """This class will predict the stock market using LSTM neural network model. Prediction will base on Close price"""

    def __init__(self, data: tuple[dict, pd.DataFrame], prediction_days: int):
        """
        :param data: data received from stock receiver
        """
        super().__init__(data, prediction_days)

        self.scaled_data: Optional[pd.DataFrame] = None
        self.x_train: Optional[np.array] = None
        self.y_train: Optional[np.array] = None
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def predict(self, last_days_close_values: np.array) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :param last_days_close_values: last days close values. Data from stock receiver without scaling and reshaping. It is done inside this method.

        :return: last days predictions
        """
        try:
            self.model = load_model(self.model_path)
        except IOError:  # FileNotFoundError from load_model
            print(f"{os.path.exists(self.model_path)=}")
            self.fit()

        scaled_last_days_close_values = self.scaler.fit_transform(last_days_close_values.reshape(-1, 1))
        prediction = self.model.predict(scaled_last_days_close_values)
        prediction = self.scaler.inverse_transform(prediction)
        return prediction[-1][0]

    def __scale_data(self):
        """
        This function will scale the data to be between 0 and 1

        :return: scaled data
        """
        self.scaled_data = self.scaler.fit_transform(self.historical_data["Close"].values.reshape(-1, 1))

    def __prepare_train_data(self):
        """
        This function will prepare the data to be trained
        """
        # country = self.thicker_info.get("country", None)
        # if country is None:
        #     raise ValueError("Country is not defined")
        x_train = []
        y_train = []
        for x in range(self.prediction_days, len(self.scaled_data)):
            x_train.append(self.scaled_data[x - self.prediction_days:x, 0])
            y_train.append(self.scaled_data[x, 0])

        self.x_train, self.y_train = np.array(x_train), np.array(y_train)
        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], self.x_train.shape[1], 1))

    def __create_model(self):
        """
        This function will create the model for the neural network
        """
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.x_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer="adam", loss="mean_squared_error")

    def fit(self):
        """
        This function will fit the data to the model
        """
        self.__scale_data()
        self.__prepare_train_data()
        self.__create_model()

        self.model.fit(self.x_train, self.y_train, epochs=25, batch_size=32)
        self.model.save(self.model_path)
        self.model.summary()
        print(self.model.summary())

    @property
    def model_path(self):
        return os.path.join(os.getcwd(), "saved_models", f"{self.name}.h5")
