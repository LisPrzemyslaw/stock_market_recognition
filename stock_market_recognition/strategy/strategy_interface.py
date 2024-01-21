from abc import ABC


class StrategyInterface(ABC):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"

    def __init__(self):
        pass

    def predict(self):
        """
        This function will predict if the stock market is ready to buy
        :return:
        """
        pass
