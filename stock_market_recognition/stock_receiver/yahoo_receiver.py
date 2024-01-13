import pandas as pd
import yfinance as yf

from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class YahooReceiver(StockReceiverInterface):
    # to use = [Close, Volume, Dividends, Stock Splits,  .info.get("country", None)]

    DEFAULT_PARAMETERS = {}

    def __init__(self):
        super().__init__()
        self.parameters = self.DEFAULT_PARAMETERS  # TODO in future

    def receive_data(self, stock_ticker: str, period="1mo", interval="1d", start=None, end=None) -> tuple[dict, pd.DataFrame]:
        """
        This method is returning data from the stock

        :param stock_ticker: name of stock ticker to receive
        :param period: Either Use period parameter or use start and end
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        :param interval: Intraday data cannot extend last 60 days
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        :param start: Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        :param end: Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"

        :return: data frame with Close, Volume, Dividends, Stock Splits, Country
        """
        ticker = yf.Ticker(stock_ticker)
        historical_data = ticker.history(period=period, interval=interval, start=start, end=end)
        return ticker.info, historical_data
