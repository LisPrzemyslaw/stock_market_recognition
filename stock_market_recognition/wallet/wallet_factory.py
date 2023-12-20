from stock_market_recognition.wallet.demo_wallet import DemoWallet


class WalletFactory:
    DEMO_WALLET = "DEMO_WALLET"
    _ALL_WALLETS = {DEMO_WALLET: DemoWallet}

    def create_wallet(self, wallet_name: str, amount: int):
        return self._ALL_WALLETS[wallet_name](amount)
