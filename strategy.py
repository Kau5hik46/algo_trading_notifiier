from pathlib import Path
from typing import List

from account import TradingAccount
from position import Position


class Strategy:
    """
    Virtual class for implementing a strategy
    """

    def __init__(self):
        self.account: TradingAccount
        self.open_positions: List[Position]

    def update(self):
        """
        (Private) method to update the strategy based on the updates from the market
        :return:
        """
        pass

    def begin_strategy(self, path: Path) -> None:
        """
        Starts the strategy when called.

        :return:
            None
        """
        trading_account = TradingAccount()
        try:
            trading_account.__load__(path)
        except:
            # TODO: Figure out what exceptions arise here and also implement the same in the trading account class
            pass

        self.strategy()

    def strategy(self):
        pass

    def end_strategy(self) -> None:
        """
        Graciously closes the strategy based on the trigger
        :return:
        """
        pass
