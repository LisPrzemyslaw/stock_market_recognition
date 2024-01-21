from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stock_market_recognition.strategy.strategy_interface import StrategyInterface


class StrategyFactory:
    _ALL_STOCK_PREDICT = {}

    @staticmethod
    def create_strategy(strategy_name: str) -> StrategyInterface:
        """
        This function will create a strategy due to given name

        :param strategy_name: name to create

        :return: stock receive class
        """
        return StrategyFactory._ALL_STOCK_PREDICT[strategy_name.upper()]()
