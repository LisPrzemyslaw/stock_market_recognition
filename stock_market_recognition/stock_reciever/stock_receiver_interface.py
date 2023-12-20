from abc import ABC, abstractmethod


class StockReceiverInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def receive_data(self):
        pass
