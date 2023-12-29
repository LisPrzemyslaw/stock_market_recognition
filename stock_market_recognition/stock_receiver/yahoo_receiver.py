import yfinance as yf

from stock_market_recognition.stock_receiver.stock_receiver_interface import StockReceiverInterface


class YahooReceiver(StockReceiverInterface):
    def __init__(self):
        super().__init__()

    def connect(self):
        pass

    def receive_data(self):
        pass
