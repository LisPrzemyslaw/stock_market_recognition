from stock_market_recognition.wallet.wallet_interface import WalletInterface


class DemoWallet(WalletInterface):
    def __init__(self, user_id: str, amount: float = 0):
        super().__init__(user_id, amount)

    def buy_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        print(f"stock: {stock_name}, bought: {amount} amount")

    def sell_stock(self, stock_name: str, amount: float):
        """
        TODO
        :param stock_name:
        :param amount:
        :return:
        """
        print(f"stock: {stock_name}, sold: {amount} amount")

