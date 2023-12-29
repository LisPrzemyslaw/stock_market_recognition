from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.wallet.wallet_interface import WalletInterface

if TYPE_CHECKING:
    from stock_market_recognition.database.database import User


class DemoWallet(WalletInterface):
    def __init__(self, db_user: User):
        super().__init__(db_user)

    def buy_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        print(f"stock: {stock_name}, bought: {amount} amount")

    def sell_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        print(f"stock: {stock_name}, sold: {amount} amount")
