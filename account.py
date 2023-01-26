from pathlib import Path
from typing import Optional, Dict, List

from exceptions import AccountException, BuyError, SellError
from security import Security


class Account:
    """
    Class that abstracts an account
    """

    def __init__(self):
        self._balance: float = 0
        self._securities: Dict[Security.name, List[int, float]] = dict()
        self._profit: float = 0

    def __load__(self, path: Path) -> None:
        pass

    def __dump__(self, path: Path) -> None:
        pass

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance

    @property
    def securities(self):
        return self._securities

    def deposit(self, amount: float = None, security: Security = None, units: int = 0):
        """
        Method to deposit money and/or securities in to the account

        :param units: int
        :param amount: float
        :param security: Security
        :return: None
        """
        if amount is None and security is None:
            raise AccountException("DEPOSIT", "Invalid deposit")

        if amount:
            self.balance += amount

        if security:
            if security not in self._securities:
                self._securities[security] = [0, 0]
            try:
                self._securities[security][1] = (self._securities[security][1] * self._securities[security][0] +
                                                 security.ltp * units)/(self._securities[security][0] + units)
                self._securities[security][0] += units
            except ZeroDivisionError:
                self._profit += (self._securities[security][1] * self._securities[security][0]
                                 + security.ltp * units)

    def withdraw(self, amount: float = None, security: Security = None, units: int = 0):
        """
        Method to withdraw money and/or securities from the account

        :param units: int
        :param amount: float
        :param security: Security
        :return: None
        """
        if amount is None and security is None:
            raise AccountException("WITHDRAWAL", "Invalid withdrawal")

        if amount:
            if amount > self.balance:
                raise AccountException("WITHDRAWAL", "Insufficient balance to withdraw")
            self.balance -= amount

        if security:
            if security.name not in self.securities:
                raise AccountException("WITHDRAWAL", "Invalid security withdrawal")
            if security not in self._securities:
                self._securities[security] = [0, 0]
            try:
                self._securities[security][1] = (self._securities[security][1] * self._securities[security][0] -
                                                 security.ltp * units) / (self._securities[security][0] - units)
                self._securities[security][0] -= units
            except ZeroDivisionError as e:
                self._profit += (self._securities[security][1] * self._securities[security][0] - security.ltp * units)


class TradingAccount(Account):
    """
    Class that inherits from an account but works as a trading account
    """

    def __init__(self):
        super().__init__()
        self._mtm: float = 0

    def buy(self, security: Security, units: int):
        """
        Method to buy the security provided
        :param security: Security to be bought
        :param units: Units of Security to be bought
        :return:
        """
        try:
            cost = security.ltp * units
            self.withdraw(amount=cost)
            self.deposit(security=security, units=units)
        except AccountException as e:
            raise BuyError(security.__repr__(), e)

    def sell(self, security: Security, units: int):
        """
        Method to sell the security provided
        :param units:
        :param security:
        :return:
        """
        try:
            cost = security.ltp * units
            self.withdraw(security=security, units=units)
            self.deposit(amount=cost)
        except AccountException as e:
            raise SellError(security.__repr__(), e)

    @property
    def mtm(self, security: Optional[Security] = None):
        """
        Method to calculate the overall MTM for the account from strategy start
        :param security:
        :return:
        """
        if security:
            # noinspection PyBroadException
            try:
                return (security.ltp - self.securities[security][1]) * self.securities[security][0]
            except Exception as e:
                raise AccountException("FETCHING_MTM_INDIVIDUAL", "Position is currently close: {}".format(e))

        mtm = 0
        for s in self.securities:
            mtm +=

    def place_order(self):
        """

        :return:
        """
        pass

    def orders(self) -> list:
        """

        :return:
        """
        pass
