from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stock_market_recognition.database.database import User


class WalletInterface(ABC):
    def __init__(self, db_user: User):
        self.db_user = db_user
        self.currency = "USD"

    @property
    def balance(self):
        return self.db_user.balance

    @balance.setter
    def balance(self, value):
        raise NotImplementedError("Not implemented")

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
