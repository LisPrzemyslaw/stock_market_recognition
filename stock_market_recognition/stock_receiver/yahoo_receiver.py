import pandas as pd
import yfinance as yf

from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class YahooReceiver(StockReceiverInterface):
    DEFAULT_PARAMETERS = {}

    def __init__(self):
        super().__init__()
        self.parameters = self.DEFAULT_PARAMETERS

    def receive_data(self, stock_name: str) -> pd.DataFrame:
        """
        This method will return the stock market due to given name and properties

        :param stock_name: name of the stock

        :return: dataframe with all data
        """
        ticker = yf.Ticker(stock_name)
