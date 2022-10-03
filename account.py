class Account():
    """
    Class that abstracts an account
    """

    def __init__(self):
        pass
    
    def deposit(self):
        pass
    
    def withdraw(self):
        pass

class TradingAccount(Account):
    """
    Class that inherits from an account but works as a trading account
    """

    def __init__(self):
        pass

    def buy(self):
        # withdraws amount and deposits the security
        try:
            self.withdraw()
            self.deposit()
        except NoBalanceException as e:
            raise BuyError("Insufficient Balance")