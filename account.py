from exceptions import AccountException


class Account():
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

    def buy(self, security: Security):
        """

        :param security:
        :return:
        """
        try:
            self.withdraw()
            self.deposit()
        except BuyError as e:
            raise AccountException("Insufficient Balance")

    def sell(self, security: Security):
        """

        :param security:
        :return:
        """
        pass

    def mtm(self, security: [Optional]):
        """

        :param security:
        :return:
        """
        pass

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