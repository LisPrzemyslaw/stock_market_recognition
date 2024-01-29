"""
This file is used to ONLY check if the code works
"""

import os
import configparser

import dotenv

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.stock_predict.lstm_stock_predict import LstmStockPredict
from stock_market_recognition.stock_predict.stock_predict_factory import StockPredictFactory
from stock_market_recognition.stock_receiver.stock_receiver_factory import StockReceiverFactory
from stock_market_recognition.wallet.wallet_factory import WalletFactory

_config = configparser.ConfigParser()
_config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))
dotenv.load_dotenv(os.path.join(os.getcwd(), "configuration", ".env"))


def __check_api():
    if not db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME")).first():
        db_session.add(
            User(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"), float(_config.get("wallet", "balance"))))
        db_session.commit()

    db_user: User = db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME")).first()
    if not db_user.verify_password(os.getenv("DB_PASSWORD")):
        raise ValueError("Incorrect password")

    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user)

    wallet.buy_stock("google", 2.1)
    wallet.sell_stock("google", 2.1)


def main():
    stock_receiver = StockReceiverFactory.create_stock_receiver(_config.get("stock_receiver", "type"))
    data = stock_receiver.receive_data("msft", period=_config.get("stock_receiver", "period"))
    stock_predict = StockPredictFactory.create_stock_predict(_config.get("stock_predict", "type"), data)
    prediction = stock_predict.predict()
    print(f"Predicted value: {prediction}")
    print(type(prediction))
    # print(type(stock_predict.scaled_data[0, 0]))


if __name__ == "__main__":
    main()
