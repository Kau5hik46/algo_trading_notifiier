class AccountException(Exception):
    error_msg = "The operation {} failed: {}"
    def __init__(self, operation: str, msg: str) -> None:
        super().__init__()
        self.error_msg = AccountException.error_msg.format(operation, msg)