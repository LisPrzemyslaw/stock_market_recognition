import os
import configparser

import dotenv

from stock_market_recognition.database.database import User, db_session
from stock_market_recognition.wallet.wallet_factory import WalletFactory


class Test:
    _configparser = configparser.ConfigParser()
    _configparser.read(os.path.join(os.getcwd(), "stock_market_recognition", "configuration", "equipment.ini"))
    dotenv.load_dotenv(os.path.join(os.getcwd(), "stock_market_recognition", "configuration", ".env"))

    def test_buy_and_sell_stocks(self):
        """
        This test verifies if user can be login to the database and then make an operations on the wallet.

        Test don't contain the assert call. If the test is not working proper exception will be raised. Otherwise,
        the test is passing without the problems.
        """
        if not db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME")).first():
            db_session.add(
                User(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"),
                     float(Test._configparser.get("wallet", "balance"))))
            db_session.commit()

        db_user: User = db_session.query(User).filter(User.user_id == os.environ.get("DB_USERNAME")).first()
        if not db_user.verify_password(os.getenv("DB_PASSWORD")):
            raise ValueError("Incorrect password")

        wallet = WalletFactory.create_wallet(Test._configparser.get("wallet", "type"), db_user)

        wallet.buy_stock("google", 2.1)
        wallet.sell_stock("google", 2.1)
