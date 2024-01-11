import pandas as pd
import yfinance as yf

from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class YahooReceiver(StockReceiverInterface):
    # to use = [Close, Volume, Dividends, Stock Splits,  .info.get("country", None)]

    DEFAULT_PARAMETERS = {}

    def __init__(self):
        super().__init__()
        self.parameters = self.DEFAULT_PARAMETERS

    def receive_data(self, stock_ticker: str) -> pd.DataFrame:
        """
        This method is returning data from the stock

        :param stock_ticker: name of stock ticker to receive

        :return: data frame with Close, Volume, Dividends, Stock Splits, Country
        """
        ticker = yf.Ticker(stock_ticker)
        historical_data = ticker.history()

