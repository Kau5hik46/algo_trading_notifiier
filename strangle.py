from datetime import date, datetime, timedelta
from typing import List, Optional

from adapter import Symbol, NSEAdapter
from constants import DATE_FORMAT
from option import Option
from position import Position
from strategy import Strategy


class Strangle(Strategy):
    """
    Class to track the market for strangle strategy

    Strategy:
        Short the 1 OTM strike on each price for the given price
        Adjustments:
            1. Keep checking if the prices of both the shorts are within the bound
            2. If the boundary is breached, trigger adjustment
            3.
    """
    NAME = "strangle"

    def __init__(self) -> None:
        super().__init__()
        self.call: Position = Position()
        self.put: Position = Position()
        self.call_hedge: Optional[Position]
        self.put_hedge: Optional[Position]

    def __set_config__(self) -> None:
        """
        Method to set the basic configurations for the strategy
        :return: None
        """
        self.SYMBOL = Symbol.BANK_NIFTY
        self.START_PRICE: float = 120.0
        self.RATIO: float = 2.0
        self.ENTRY_DATE_TIME: datetime = datetime.now().replace(hour=13, minute=25, second=0) + \
                                         timedelta(days=(3-datetime.now().weekday())%7)
        self.EXPIRY_DATE: date = (self.ENTRY_DATE_TIME + timedelta(days=7)).date()
        self.adapter = NSEAdapter(self.SYMBOL)

    def strategy(self):
        """
        Actual strategy implementation with the golden rules
        :return:
        """
        # Adjustment
        ratio = self.call.security.ltp / self.put.security.ltp
        if ratio > self.RATIO or ratio < (1/self.RATIO):
            # Trigger adjustment
            self.adjust()


    # Exit

    def end_strategy(self) -> None:
        """
        Graciously closes the strategy based on the trigger
        :return:
        """
        pass

    def __

    def entry(self):
        """
        Method to enter the strategy for the first time
        :return:
        """
        # Trigger on thursday at or after 1:15 PM
        if self.ENTRY_DATE_TIME <= datetime.now() < self.ENTRY_DATE_TIME + timedelta(minutes=5):
            call_option_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                         expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                         option_type="CE", ltp=self.START_PRICE)
            put_option_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                        expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                        option_type="PE", ltp=self.START_PRICE)
            call_option = Option(call_option_params)
            put_option = Option(put_option_params)

    def adjust(self):
        pass
