import pytest
import os
import configparser

import dotenv

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.wallet.wallet_factory import WalletFactory
from stock_market_recognition.stock_predict.stock_predict_factory import StockPredictFactory
from stock_market_recognition.stock_receiver.stock_receiver_factory import StockReceiverFactory


class Test:
    """Constants"""
    PREDICTION_DAYS = 7
    STOCK_TICKERS = ("msft",)

    """Configurations"""
    _configparser = configparser.ConfigParser()
    _configparser.read(os.path.join(os.getcwd(), "stock_market_recognition", "configuration", "equipment.ini"))
    dotenv.load_dotenv(os.path.join(os.getcwd(), "stock_market_recognition", "configuration", ".env"))

    @pytest.mark.parametrize("p_stock_ticker", STOCK_TICKERS)
    def test_predict_value(self, p_stock_ticker):
        """

        """
        ########################################################################
        # CONDITION
        ########################################################################
        stock_receiver = StockReceiverFactory.create_stock_receiver(Test._configparser.get("stock_receiver", "type"))
        data = stock_receiver.receive_data(p_stock_ticker, period=Test._configparser.get("stock_receiver", "period"))
        stock_predictor = StockPredictFactory.create_stock_predict(Test._configparser.get("stock_predict", "type"), data, Test.PREDICTION_DAYS)

        # Only for test purposes
        last_days_close_value = data[1]["Close"].values[-Test.PREDICTION_DAYS:]
        real_value = data[1]['Close'].values[-1]

        ########################################################################
        # ACTION
        ########################################################################
        """
        For the test purposes it is needed to call fit(). In the normal usecase it will be enough to call only predict().
        The predict calls fit if the model is not saved.
        """
        stock_predictor.fit()
        prediction = stock_predictor.predict(last_days_close_value)
        ########################################################################
        # EXPECTATION
        ########################################################################
        # Hard to test the values. The comparison must be done by tester.
        print(f"Predicted value: {prediction}")
        print(f"Real value: {real_value}")
        print(f"MSE: {(prediction - real_value)**2}")
