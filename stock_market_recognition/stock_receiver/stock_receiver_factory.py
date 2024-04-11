from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.stock_receiver.yahoo_receiver import YahooReceiver

if TYPE_CHECKING:
    from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class StockReceiverFactory:
    _ALL_STOCK_PREDICT = {"YAHOO": YahooReceiver}

    @staticmethod
    def create_stock_receiver(receiver_name: str) -> StockReceiverInterface:
        """
        This function will create a stock predict due to given name

        :param receiver_name: name to create (neural network or regression)

        :return: stock receive class
        """
        return StockReceiverFactory._ALL_STOCK_PREDICT[receiver_name.upper()]()
