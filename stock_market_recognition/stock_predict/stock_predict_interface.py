from abc import ABC, abstractmethod


class StockPredictInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def predict(self):
        pass
