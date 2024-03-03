from typing import Optional

import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
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
        self.x_test: np.array = self.historical_data["Close"].values[-self.prediction_days:].reshape(-1, 1)
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def predict(self) -> np.array:
        """
        This function will predict if the stock market is ready to buy

        :return: last days predictions
        """
        self.__scale_data()
        self.__prepare_train_data()
        self.__create_model()

        self.fit()
        prediction = self.model.predict(self.x_test)
        prediction = self.scaler.inverse_transform(prediction)
        return prediction

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
        self.model.fit(self.x_train, self.y_train, epochs=25, batch_size=32)
        self.model.save("model.h5")
        self.model.summary()
        print(self.model.summary())
