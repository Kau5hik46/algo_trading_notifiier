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


class SellError(Exception):
    error_msg = "Selling {} failed: {}"

    def __init__(self, instrument: str, reason: str) -> None:
        super().__init__()
        self.error_msg = SellError.error_msg.format(instrument, reason)


class OrderError(Exception):
    error_msg = "Order execution failed: {} failed: {}"

    def __init__(self, instrument: str, reason: str) -> None:
        super().__init__()
        self.error_msg = OrderError.error_msg.format(instrument, reason)
