import copy
import os
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Model, Sequential, load_model

from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface


class LstmStockPredict(StockPredictInterface):
    """This class will predict the stock market using LSTM neural network model. Prediction will base on Close price"""

    def __init__(
            self,
            data: tuple[dict, pd.DataFrame],
            prediction_days: int,
            lstm_units: int = 50,
            dropout: float = 0.2,
            epoch: int = 25,
            batch_size: int = 32
    ):
        """
        :param data: data received from stock receiver
        :param prediction_days: number of days to predict
        :param lstm_units: number of units in LSTM layer
        :param dropout: dropout value
        :param epoch: number of epochs
        :param batch_size: batch size
        """
        super().__init__(data, prediction_days)

        self.scaled_data: Optional[pd.DataFrame] = None
        self.x_train: Optional[np.array] = None
        self.y_train: Optional[np.array] = None
        self.model: Optional[Model] = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        """Model parameters"""
        self.lstm_units = lstm_units
        self.dropout = dropout
        self.epoch = epoch
        self.batch_size = batch_size
        # TODO add more lstm layers and analyze the results

        """mse"""
        self.mse: float | None = None
        self.mse_scaled: float | None = None

    def predict(self, last_days_close_values: np.array, fit_model=False) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :param last_days_close_values: last days close values. Data from stock receiver without scaling and reshaping. It is done inside this method.
        :param fit_model: if True the model will be fitted

        :return: last days predictions
        """
        if fit_model:
            self.fit()
        else:  # Try to load model from file, if not exists fit the model
            try:
                self.model = load_model(self.model_path)
            except IOError:  # FileNotFoundError from load_model
                print(f"{os.path.exists(self.model_path)=}")
                self.fit()

        scaled_last_days_close_values = self.scaler.fit_transform(last_days_close_values.reshape(-1, 1))
        prediction = self.model.predict(scaled_last_days_close_values)
        prediction_scaled = copy.deepcopy(prediction)
        prediction = self.scaler.inverse_transform(prediction)
        last_days_close_values_reshaped = last_days_close_values.reshape(-1, 1)
        self.mse = mean_squared_error(last_days_close_values_reshaped, prediction)
        self.mse_scaled = mean_squared_error(scaled_last_days_close_values, prediction_scaled)
        return prediction[-1][0]

    def __scale_data(self) -> None:
        """This function will scale the data to be between 0 and 1"""
        self.scaled_data = self.scaler.fit_transform(self.historical_data["Close"].values.reshape(-1, 1))

    def __prepare_train_data(self) -> None:
        """This function will prepare the data to be trained"""
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

    def __create_model(self) -> None:
        """This function will create the model for the neural network"""
        self.model = Sequential()
        self.model.add(LSTM(units=self.lstm_units, return_sequences=True, input_shape=(self.x_train.shape[1], 1)))
        self.model.add(Dropout(self.dropout))
        self.model.add(LSTM(units=self.lstm_units, return_sequences=True))
        self.model.add(Dropout(self.dropout))
        self.model.add(LSTM(units=self.lstm_units))
        self.model.add(Dropout(self.dropout))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer="adam", loss="mean_squared_error")

    def fit(self) -> None:
        """This function will fit the data to the model"""
        self.__scale_data()
        self.__prepare_train_data()
        self.__create_model()

        self.model.fit(self.x_train, self.y_train, epochs=self.epoch, batch_size=self.batch_size)
        self.model.save(self.model_path)
        self.model.summary()
        print(self.model.summary())

    @property
    def model_path(self):
        return os.path.join(os.getcwd(), "saved_models", f"{self.name}.h5")
