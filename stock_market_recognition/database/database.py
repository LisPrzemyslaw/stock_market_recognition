import os
import hashlib
import configparser

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Float, Column, String, ForeignKey, create_engine

_Base = declarative_base()


class Stock(_Base):
    __tablename__ = "stock"

    user_id = Column("user_id", ForeignKey("user.user_id"), primary_key=True)
    stock_name = Column("stock_name", String)
    stock_amount = Column("stock_amount", Float)

    def __init__(self, user_id: str, stock_name: str, stock_amount: float):
        self.user_id = user_id
        self.stock_name = stock_name
        self.stock_amount = stock_amount

    def __repr__(self):
        return f"<Stock {self.user_id}> ({self.stock_name}: {self.stock_amount})"


class User(_Base):
    __tablename__ = "user"

    user_id = Column("user_id", String, primary_key=True)
    password = Column("password", String)
    balance = Column("balance", Float)

    def __init__(self, user_id: str, password: str, balance: float) -> None:
        self.user_id = user_id
        self.password = self.__encode_password(password)
        self.balance = balance

    @staticmethod
    def __encode_password(password: str) -> str:
        """
        This function is used to encode password

        :param password: original given password

        :return: hashed password
        """
        password_bytes = password.encode("utf-8")
        hasher = hashlib.sha256()
        hasher.update(password_bytes)
        hashed_password = hasher.hexdigest()
        return hashed_password

    def verify_password(self, password: str) -> bool:
        """
        This function is used to verify if password is proper

        :param password: given password

        :return: boolean if password is the same as in database
        """
        return self.__encode_password(password) == self.password

    def __repr__(self):
        return f"<User {self.user_id}> {self.balance} USD"


def _choose_database() -> str:
    """
    This function will return proper db due to config

    :return: database path
    """
    _config = configparser.ConfigParser()
    _config.read(os.path.join(os.getcwd(), "configuration", "equipment.ini"))
    db_type = _config.get("database", "type")
    if db_type == "local":
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "stock.db")
    raise NotImplementedError


_engine = create_engine(f"sqlite:///{_choose_database()}", echo=False)  # echo=True --> debug purposes
_Base.metadata.create_all(bind=_engine)
_Session = sessionmaker(bind=_engine)

db_session = _Session()
