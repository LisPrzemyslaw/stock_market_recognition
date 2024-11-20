from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.stock_receiver.yahoo_receiver import YahooReceiver

if TYPE_CHECKING:
    from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class StockReceiverFactory:
    __STOCK_RECEIVER = None

    _ALL_STOCK_PREDICT = {"YAHOO": YahooReceiver}
    __DEFAULT_STOCK_RECEIVER = "YAHOO"

    @staticmethod
    def create_stock_receiver(receiver_name: str) -> StockReceiverInterface:
        """
        This function will create a stock predict due to given name

        :param receiver_name: name to create (neural network or regression)

        :return: stock receive class
        """
        StockReceiverFactory.__STOCK_RECEIVER = StockReceiverFactory._ALL_STOCK_PREDICT[receiver_name.upper()]()
        return StockReceiverFactory.__STOCK_RECEIVER

    @staticmethod
    def get_stock_receiver() -> StockReceiverInterface:
        """
        This function will return stock receiver

        :return: stock receiver
        """
        if not StockReceiverFactory.__STOCK_RECEIVER:
            return StockReceiverFactory.create_stock_receiver(StockReceiverFactory.__DEFAULT_STOCK_RECEIVER)
        return StockReceiverFactory.__STOCK_RECEIVER
