from stock_market_recognition.wallet.wallet_interface import WalletInterface


class DemoWallet(WalletInterface):
    def __init__(self, amount: int = 0):
        super().__init__(amount)

    def buy_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        pass

    def sell_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        pass
