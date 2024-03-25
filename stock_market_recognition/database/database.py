import os
import hashlib
import configparser
from datetime import datetime, timedelta
from uuid import uuid4, UUID
import secrets
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Float, Column, String, ForeignKey, create_engine

_Base = declarative_base()


class Stock(_Base):
    __tablename__ = "stock"

    user_id = Column("user_id", ForeignKey("user.user_id"), primary_key=True)
    stock_name = Column("stock_name", String)
    stock_amount = Column("stock_amount", Float)

    def __init__(self, wallet_id: str, stock_name: str, stock_amount: float):
        self.wallet_id = wallet_id
        self.stock_name = stock_name
        self.stock_amount = stock_amount

    def __repr__(self):
        return f"<Stock {self.stock_id}> ({self.stock_name}: {self.stock_amount})"


class User(_Base):
    __tablename__ = "user"

    AUTH_TIME = 10  # minutes

    user_id = Column("user_id", String, primary_key=True)
    password = Column("password", String)
    balance = Column("balance", Float)

    def __init__(self, user_id: str, password: str, balance: float) -> None:
        self.user_id = user_id
        self.password = self.__encode_password(password)
        self.balance = balance

        self.__auth_token = None
        self.__token_creation_time = None

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

    @property
    def auth_token(self) -> UUID | None:
        """
        This function is used to get auth token

        :return: auth token
        """
        if self.__token_creation_time is None:
            self.__auth_token = None  # To be sure that both are set at the same time
            return None
        if self.__token_creation_time + timedelta(minutes=self.AUTH_TIME) > datetime.now():
            self.__auth_token = None
        return self.__auth_token

    def create_auth_token(self) -> UUID:
        """
        This function is used to create auth token

        :return: auth token
        """
        if self.auth_token is None:
            self.__token_creation_time = datetime.now()
            self.__auth_token = uuid4()
            self.__auth_token = secrets.token_hex()  # TODO
        return self.auth_token

    def is_auth(self, auth_token: UUID) -> bool:
        """
        This function is used to check if user is authenticated

        :param auth_token: given auth token

        :return: boolean if user is authenticated
        """
        return self.auth_token == auth_token

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
