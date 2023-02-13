import pickle
from datetime import date
from pathlib import Path
from typing import List

from accounting.account import TradingAccount
from accounting.position import Position
from adapter.adapter import NSEAdapter
from exceptions.account_exceptions import LoadError


class Strategy:
    """
    Virtual class for implementing a manager
    """
    NAME: str = "strategy_name"

    def __init__(self):
        self.EXPIRY_DATE: date = date.today()
        self.adapter: NSEAdapter
        self.BEGIN_DATE: date = date.today()
        self.account: TradingAccount = TradingAccount()
        self._open_positions: List[Position] = list()
        self.save_path: Path

    def __str__(self):
        return "{}_{}.dump".format(self.NAME, self.EXPIRY_DATE)

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
        try:
            self._load_strategy(path)
            print(self.account)
            return None
        except LoadError as e:
            # TODO: Figure out what exceptions arise here and also implement the same in the trading account class
            self.entry()
            print(self.account)

    def strategy(self):
        pass

    def _load_strategy(self, path: Path):
        """
        Method to load the strategy from a pickle at the start of the day
        Returns
        -------

        """
        try:
            with open(path, 'rb') as input_path:
                strategy = pickle.load(input_path)
                self.__dict__.update(strategy.__dict__)
        except FileNotFoundError as e:
            raise LoadError("LOAD", e.__str__())

    def _save_strategy(self, path: Path):
        """
        Method to save the strategy as a pickle at the end of the day
        Returns
        -------

        """
        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def end_strategy(self) -> None:
        """
        Graciously closes the manager based on the trigger
        :return:
        """
        pass
