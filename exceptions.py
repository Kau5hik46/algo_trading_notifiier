class Exception_(Exception):
    def __str__(self) -> str:
        return super().__str__()

class AccountException(Exception):
    error_msg = "The operation {} failed: {}"
    def __init__(self, operation: str, msg: str) -> None:
        super().__init__()
        self.error_msg = AccountException.error_msg.format(operation, msg)
        
class BuyError(Exception):
    error_msg = "Buying {} failed: {}"
    def __init__(self, instrument: str, reason: str) -> None:
        super().__init__()
        self.error_msg = BuyError.error_msg.format(instrument, reason)