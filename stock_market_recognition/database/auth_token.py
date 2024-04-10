import secrets
from datetime import timedelta, datetime
from uuid import UUID


class AuthToken:
    AUTH_TIME = 10  # minutes

    def __init__(self):
        self.__auth_token = None
        self.__token_creation_time = None

        self._create_auth_token()

    @property
    def auth_token(self) -> str | None:
        """
        This function is used to get auth token

        :return: auth token
        """
        if self.__token_creation_time is None:
            self.__auth_token = None  # To be sure that both are set at the same time
            return None
        if self.__token_creation_time + timedelta(minutes=self.AUTH_TIME) < datetime.now():
            self.__auth_token = None
        return self.__auth_token

    def _create_auth_token(self) -> str:
        """
        This function is used to create auth token

        :return: auth token
        """
        if self.auth_token is None:
            self.__token_creation_time = datetime.now()
            self.__auth_token = secrets.token_hex()
        return self.auth_token

    def is_auth(self, auth_token: str) -> bool:
        """
        This function is used to check if user is authenticated

        :param auth_token: given auth token

        :return: boolean if user is authenticated
        """
        if self.auth_token is None:
            return False  # To be sure that we are not compare None == None
        return self.auth_token == auth_token


class AuthTokenContainer:
    __AUTH_TOKENS: dict[str, AuthToken] = {}

    @staticmethod
    def add_token(user_id: str) -> str:
        """
        This function create token and returns it.

        :param user_id: user id

        :return: auth token
        """
        AuthTokenContainer.__AUTH_TOKENS[user_id] = AuthToken()
        return AuthTokenContainer.__AUTH_TOKENS[user_id].auth_token

    @staticmethod
    def is_user_auth(user_id: str, token: str) -> bool:
        """
        Check if user has token
        """
        try:
            auth_token = AuthTokenContainer.__AUTH_TOKENS[user_id]
            return auth_token.is_auth(token)
        except KeyError:
            return False
