class AdapterError(Exception):
    error_msg = "The operation {} failed: {}"

    def __init__(self, operation: str, msg: str) -> None:
        super().__init__()
        self.error_msg = AdapterError.error_msg.format(operation, msg)


class OptionNotFoundError(Exception):
    error_msg = "The option {} was not found: {}"

    def __init__(self, option_id: str, msg: str) -> None:
        super().__init__()
        self.error_msg = AdapterError.error_msg.format(option_id, msg)
