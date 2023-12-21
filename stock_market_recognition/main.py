"""
There will be flask api for this app
"""
import os
import uuid
import configparser
import dotenv
from stock_market_recognition.database.database import db_session, User
from stock_market_recognition.wallet.wallet_factory import WalletFactory


def main():
    # Test API
    dotenv.load_dotenv(os.path.join(os.getcwd(), "configuration", '.env'))
    _config = configparser.ConfigParser()
    _config.read(os.path.join(os.getcwd(), "configuration", 'equipment.ini'))

    if db_session.query(User).filter(User.user_id == os.environ.get('DB_USERNAME')).count() == 0:
        db_session.add(
            User(os.environ.get('DB_USERNAME'), os.environ.get('DB_PASSWORD'), float(_config.get("wallet", "balance"))))
        db_session.commit()

    db_user: User = db_session.query(User).filter(User.user_id == os.environ.get('DB_USERNAME'))[0]
    if not db_user.verify_password(os.getenv('DB_PASSWORD')):
        raise ValueError('Incorrect password')

    wallet = WalletFactory.create_wallet(_config.get("wallet", "type"), db_user.user_id, db_user.balance)

    wallet.buy_stock("google", 2.1)
    wallet.sell_stock("google", 2.1)


if __name__ == "__main__":
    main()
