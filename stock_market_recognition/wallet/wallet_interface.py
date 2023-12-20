from abc import ABC, abstractmethod

# import sqlalchemy


class WalletInterface(ABC):
    def __init__(self, amount: int = 0):
        self.currency = "USD"
        self.amount = amount
        self.stocks: dict[str: float] = {}  # In database with sqlalchemy. If exist then increade, decrease

    @abstractmethod
    def buy_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        pass

    @abstractmethod
    def sell_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        pass
