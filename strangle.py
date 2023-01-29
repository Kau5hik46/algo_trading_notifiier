from account import TradingAccount
from strategy import Strategy


class Strangle(Strategy):
    """
    Class to track the market for strangle strategy
    """

    def __init__(self) -> None:
        super().__init__()
        self.strikes_ltp: float = 120

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

    def strategy(self):
        """
        Actual strategy implementation with the golden rules
        :return:
        """


    def end_strategy(self) -> None:
        """
        Graciously closes the strategy based on the trigger
        :return:
        """
        pass

    def __