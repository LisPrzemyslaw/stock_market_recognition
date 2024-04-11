from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.stock_predict.lstm_stock_predict import LstmStockPredict

if TYPE_CHECKING:
    import pandas as pd

    from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface


class StockPredictFactory:
    _ALL_STOCK_PREDICT = {"LSTM": LstmStockPredict}

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
