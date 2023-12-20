from stock_market_recognition.wallet.wallet_interface import WalletInterface

class DemoWallet(WalletInterface):
    def __init__(self, amount: int = 0):
        super().__init__(amount)
