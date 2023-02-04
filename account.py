from exceptions import *
from utility.parameter_dataclasses import *


class Account:
    """
    Class that abstracts an account
    """

    def __init__(self):
        pass

    def deposit(self, security):
        pass

    def withdraw(self):
        pass


class TradingAccount(Account):
    """
    Class that inherits from an account but works as a trading account
    """

    def __init__(self):
        pass

    def deposit(self, security):
        pass

    def buy(self, security: Security):
        # withdraws amount and deposits the security
        try:
            self.withdraw()
            self.deposit()
        except BuyError as e:
            raise AccountException("Insufficient Balance")
