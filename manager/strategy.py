from datetime import date
from pathlib import Path
from typing import List

from accounting.account import TradingAccount
from adapter import NSEAdapter
from accounting.position import Position


class Strategy:
    """
    Virtual class for implementing a manager
    """
    NAME: str = "strategy_name"

    def __init__(self, account: TradingAccount):
        self.adapter: NSEAdapter
        self.BEGIN_DATE: date = date.today()
        self.account: TradingAccount = TradingAccount()
        self.open_positions: List[Position] = list()
        self.save_path: Path

    def __str__(self):
        return "{}_{}.dump".format(self.NAME, self.BEGIN_DATE)

    def update(self):
        """
        Method to update the manager based on the updates from the market
        :return:
        """
        pass

    def entry(self):
        """
        Method to run only if the manager is new!
        :return:
        """
        pass

    def exit(self):
        """
        Method to run when exit condition is triggered
        :return:
        """
        pass

    def begin_strategy(self, path: Path) -> None:
        """
        Starts the manager when called.

        :return:
            None
        """
        trading_account = TradingAccount()
        try:
            trading_account.__load__(path)
            return None
        except:
            # TODO: Figure out what exceptions arise here and also implement the same in the trading account class
            self.entry()


    def strategy(self):
        pass

    def end_strategy(self) -> None:
        """
        Graciously closes the manager based on the trigger
        :return:
        """
        pass