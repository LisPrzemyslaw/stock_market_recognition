"""
This file is used to ONLY check if the code works
"""

import os
import configparser

import dotenv
import matplotlib.pyplot as plt

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.stock_predict.stock_predict_factory import StockPredictFactory
from stock_market_recognition.stock_receiver.stock_receiver_factory import StockReceiverFactory
from stock_market_recognition.wallet.wallet_factory import WalletFactory

_config = configparser.ConfigParser()
_config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))
dotenv.load_dotenv(os.path.join(os.getcwd(), "configuration", ".env"))

"""Constants"""
PREDICTION_DAYS = 7
STOCK_TICKERS = ("msft",)

"""Constants but variables :)"""
STOCK_PREDICTORS = {}


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
    for stock_ticker in STOCK_TICKERS:
        data = stock_receiver.receive_data(stock_ticker, period=_config.get("stock_receiver", "period"))
        STOCK_PREDICTORS[stock_ticker] = StockPredictFactory.create_stock_predict(_config.get("stock_predict", "type"), data, PREDICTION_DAYS)

        # Only for test purpouses
        last_days_close_value = data[1]["Close"].values[-PREDICTION_DAYS:]
        real_value = data[1]['Close'].values[-1]

    # COMMENT IF NEEDED
    # STOCK_PREDICTORS[STOCK_TICKERS[0]].fit()

    prediction = STOCK_PREDICTORS[STOCK_TICKERS[0]].predict(last_days_close_value)
    print(f"Predicted value: {prediction}")
    print(f"Real value: {real_value}")


if __name__ == "__main__":
    main()
