from __future__ import annotations
from typing import TYPE_CHECKING

from stock_market_recognition.stock_predict.lstm_stock_predict import LstmStockPredict

if TYPE_CHECKING:
    from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface
    import pandas as pd


class StockPredictFactory:
    __STOCK_RECEIVER = None

    _ALL_STOCK_PREDICT = {"LSTM": LstmStockPredict}
    __DEFAULT_STOCK_PREDICT = "LSTM"

    @staticmethod
    def create_stock_predict(predict_name: str, data: tuple[dict, pd.DataFrame], prediction_days: int) -> StockPredictInterface:
        """
        This function will create a stock predict due to given name

        :param predict_name: name to create (neural network or regression)
        :param data: data to proceed. Received from stock receiver
        :param prediction_days: how many days to predict

        :return: stock predict class
        """
        return StockPredictFactory._ALL_STOCK_PREDICT[predict_name.upper()](data, prediction_days)

    @staticmethod
    def get_stock_predict() -> StockPredictInterface:
        """
        This function will return stock predict

        :return: stock predict
        """
        if not StockPredictFactory.__STOCK_RECEIVER:
            return StockPredictFactory.create_stock_predict(StockPredictFactory.__DEFAULT_STOCK_PREDICT)
        return StockPredictFactory.__STOCK_RECEIVER
