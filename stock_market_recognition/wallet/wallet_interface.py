from abc import ABC, abstractmethod

# import sqlalchemy


class WalletInterface(ABC):
    def __init__(self, amount: float = 0):
        self.currency = "USD"
        self.amount = amount

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

    # @
    # def all_stocks(self):
    #     return
