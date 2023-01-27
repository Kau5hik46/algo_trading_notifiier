from account import TradingAccount


class Strangle():
    """
    Class to track the market for strangle strategy
    """

    def __init__(self) -> None:
        pass
    
    def begin_strategy(self) -> None:
        """
        Starts the strategy when called.

        :return:
            None
        """
        trading_account = TradingAccount()
        try:
            trading_account.__load__(Path("data.dumo"))
        except

    def end_strategy(self) -> None:
        """
        Graciously closes the strategy based on the trigger
        :return:
        """
        pass

    def __