from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.wallet.wallet_interface import WalletInterface

if TYPE_CHECKING:
    from stock_market_recognition.database.database import User


class DemoWallet(WalletInterface):
    def __init__(self, db_user: User):
        super().__init__(db_user)

    def buy_stock(self, stock_name: str, amount: float) -> None:
        """
        This method is used to buy a stock

        :param stock_name: name of the stock
        :param amount: amount to buy
        """
        print(f"stock: {stock_name}, bought: {amount} amount")

    def sell_stock(self, stock_name: str, amount: float) -> None:
        """
        This method is used to sell a stock

        :param stock_name: name of the stock
        :param amount: amount to sell
        """
        print(f"stock: {stock_name}, sold: {amount} amount")

    def get_all_stocks(self) -> dict[str, float]:
        """
        This function will return all stocks assigned to this user.

        :return: dict of all stocks assigned to this wallet
        """
        return {}  # TODO
