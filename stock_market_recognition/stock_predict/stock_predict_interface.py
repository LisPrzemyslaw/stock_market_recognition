from abc import ABC, abstractmethod


class StockPredictInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def predict(self) -> str:
        """
        This function will predict if the stock market is ready to buy

        :return: string "BUY", "SELL", or "WAIT"
        """
        pass


class Prediction:
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"
