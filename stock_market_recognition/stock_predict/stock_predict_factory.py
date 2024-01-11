from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stock_market_recognition.stock_predict.stock_predict_interface import StockPredictInterface


class StockPredictFactory:
    _ALL_STOCK_PREDICT = {}

    @staticmethod
    def create_stock_predict(predict_name: str) -> StockPredictInterface:
        """
        This function will create a stock predict due to given name

        :param predict_name: name to create (neural network or regression)

        :return: stock predict class
        """
        return StockPredictFactory._ALL_STOCK_PREDICT[predict_name]()
