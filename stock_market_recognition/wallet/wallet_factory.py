from __future__ import annotations

from typing import TYPE_CHECKING
from stock_market_recognition.wallet.demo_wallet import DemoWallet

if TYPE_CHECKING:
    from stock_market_recognition.wallet.wallet_interface import WalletInterface


class WalletFactory:
    DEMO_WALLET = "DEMO_WALLET"
    _ALL_WALLETS = {DEMO_WALLET: DemoWallet}

    @staticmethod
    def create_wallet(wallet_name: str, user_id: str, amount: float) -> WalletInterface:
        return WalletFactory._ALL_WALLETS[wallet_name](user_id, amount)
