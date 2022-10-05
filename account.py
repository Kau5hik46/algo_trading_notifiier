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
    
    def deposit(self, security):
        

    def buy(self, security: Security):
        # withdraws amount and deposits the security
        try:
            self.withdraw()
            self.deposit()
        except AccountException as e:
            raise BuyError("Insufficient Balance")
        