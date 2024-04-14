from __future__ import annotations

from typing import TYPE_CHECKING

from stock_market_recognition.wallet.wallet_interface import WalletInterface
from stock_market_recognition.database.database import db_session, Stock
from stock_market_recognition.stock_receiver.stock_receiver_factory import StockReceiverFactory
if TYPE_CHECKING:
    from stock_market_recognition.database.database import User


class DemoWallet(WalletInterface):
    __TICKER_INFO_INDEX = 0

    def __init__(self, db_user: User):
        super().__init__(db_user)
        self.stock_receiver = StockReceiverFactory.get_stock_receiver()

    def buy_stock(self, stock_name: str, amount: float) -> None:
        """
        This method is used to buy a stock

        :param stock_name: name of the stock
        :param amount: amount to buy
        """
        db_stock: Stock = db_session.query(Stock).filter(Stock.user_id == self.db_user.user_id, Stock.stock_name == stock_name).first()
        current_stock_price = self.stock_receiver.receive_data(stock_name)[self.__TICKER_INFO_INDEX]["currentPrice"]
        if self.balance - current_stock_price * amount < 0:
            raise ValueError("Not enough money to buy this stock")

        self.balance = self.balance - current_stock_price * amount
        if db_stock:
            db_stock.stock_amount += amount
        else:
            db_stock = Stock(self.db_user.user_id, stock_name, amount)
            db_session.add(db_stock)
        db_session.commit()

    def sell_stock(self, stock_name: str, amount: float) -> None:
        """
        This method is used to sell a stock

        :param stock_name: name of the stock
        :param amount: amount to sell
        """
        db_stock: Stock = db_session.query(Stock).filter(Stock.user_id == self.db_user.user_id, Stock.stock_name == stock_name).first()
        if not db_stock:
            raise ValueError("No such stock in wallet")
        if db_stock.stock_amount < amount:
            raise ValueError("Not enough stock to sell")

        current_stock_price = self.stock_receiver.receive_data(stock_name)[self.__TICKER_INFO_INDEX]["currentPrice"]
        self.balance = self.balance + current_stock_price * amount
        db_stock.stock_amount -= amount
        db_session.commit()

    def get_all_stocks(self) -> dict[str, float]:
        """
        This function will return all stocks assigned to this user.

        :return: dict of all stocks assigned to this wallet
        """
        raise NotImplementedError("This method is not implemented yet")
