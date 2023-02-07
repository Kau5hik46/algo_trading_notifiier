import math
from datetime import date, datetime, timedelta
from typing import List, Optional

from accounting.account import TradingAccount
from accounting.position import Position
from adapter.adapter import Symbol, NSEAdapter
from constants import DATE_FORMAT
from entity.position_properties import PositionDirection, PositionSide
from instruments.option import Option
from manager.strategy import Strategy


class Strangle(Strategy):
    """
    Class to track the market for strangle manager

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
        self.call_hedge: Optional[Position] = Position()
        self.put_hedge: Optional[Position] = Position()

    @property
    def open_positions(self) -> List[Position]:
        """
        Getter for open positions
        :return: List of all open Positions
        """
        self._open_positions = list([self.call, self.put, self.call_hedge, self.put_hedge])
        return self._open_positions

    def __set_config__(self) -> None:
        """
        Method to set the basic configurations for the manager
        :return: None
        """
        self.SYMBOL = Symbol.BANK_NIFTY
        self.LOT_SIZE: int = 25
        self.LOTS: int = 1
        self.START_PRICE: float = 120.0
        self.HEDGE_START_PRICE: float = 20.0
        self.RATIO: float = 2.0
        self.ENTRY_DATE_TIME: datetime = datetime.now().replace(hour=13, minute=25, second=0) + \
                                         timedelta(days=(3 - datetime.now().weekday()) % 7)
        self.EXPIRY_DATE: date = (self.ENTRY_DATE_TIME + timedelta(days=7)).date()
        self.STRADDLE_STOP_LOSS_RATIO: float = 1.3
        self.CURRENT_STOP_LOSS = math.inf
        self.EXIT_PROFIT: float = 4000
        self.adapter = NSEAdapter(self.SYMBOL)

    def entry(self):
        """
        Method to enter the manager for the first time
        :return:
        """
        # TODO: Trigger on thursday at or after 1:15 PM
        call_option_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                     expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                     option_type="CE", ltp=self.START_PRICE)
        put_option_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                    expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                    option_type="PE", ltp=self.START_PRICE)
        call_option_hedge_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                           expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                           option_type="CE", ltp=self.HEDGE_START_PRICE)
        put_option__hedge_params = self.adapter.get_option(underlying=self.SYMBOL,
                                                           expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
                                                           option_type="PE", ltp=self.HEDGE_START_PRICE)

        call_option = Option(**call_option_params)
        call_hedge = Option(**call_option_hedge_params)
        put_option = Option(**put_option_params)
        put_hedge = Option(**put_option__hedge_params)

        self.call_hedge = Position(call_hedge, PositionSide.BUY, PositionDirection.LONG, self.LOTS * self.LOT_SIZE)
        self.put_hedge = Position(put_hedge, PositionSide.BUY, PositionDirection.SHORT, self.LOTS * self.LOT_SIZE)
        self.call = Position(call_option, PositionSide.SELL, PositionDirection.SHORT, self.LOTS * self.LOT_SIZE)
        self.put = Position(put_option, PositionSide.SELL, PositionDirection.LONG, self.LOTS * self.LOT_SIZE)

        # self.account.order_from_position(self.call_hedge)
        # self.account.order_from_position(self.put_hedge)
        self.account.order_from_position(self.call)
        self.account.order_from_position(self.put)

    def _secondary_adjust(self, square_off_leg: Position, reference_leg: Position) -> None:
        """
        Method to run the straddle adjustment when leg A and leg B have same strike-prices
        sets the self.STOP_LOSS and when the stop loss is breached, calls the self.exit()
        Parameters
        ----------
        square_off_leg
        reference_leg

        :return: None
        -------
        """
        self.CURRENT_LTP_SUM = square_off_leg.security.ltp + reference_leg.security.ltp

        if self.CURRENT_STOP_LOSS is math.inf:
            self.CURRENT_STOP_LOSS = self.CURRENT_LTP_SUM * self.STRADDLE_STOP_LOSS_RATIO

        if self.CURRENT_LTP_SUM >= self.CURRENT_STOP_LOSS:
            self.exit()

    def adjust(self, square_off_leg: Position, reference_leg: Position) -> Position:
        """
        Method to adjust the strategy based on the market conditions

        :param reference_leg:
        :param square_off_leg:
        :return:
        """

        if square_off_leg.security.strike_price == reference_leg.security.strike_price:
            self._secondary_adjust(square_off_leg, reference_leg)
            return square_off_leg
        # Square off the existing position and take a new position
        square_off_leg.side = PositionSide.SQUARE_OFF
        # Placing the order from Position
        self.account.order_from_position(square_off_leg)

        # Fetching the relevant option from the Adapter
        adjusted_option = self.adapter.get_option(
            underlying=self.SYMBOL,
            expiry_date=self.EXPIRY_DATE.strftime(DATE_FORMAT),
            option_type=square_off_leg.security.option_type,
            ltp=reference_leg.security.ltp
        )
        # noinspection PyTypeChecker
        # Creating a new position in the place of existing position
        adjusted_position = Position(adjusted_option, square_off_leg.side, square_off_leg.direction,
                                     square_off_leg.quantity)

        # Placing the order from Position
        self.account.order_from_position(adjusted_position)

        del square_off_leg
        return adjusted_position

    def exit(self):
        """
        Method to square off all the open positions and wait for the entry of next manager
        :return:
        """
        for position in self.open_positions:
            position.side = PositionSide.SQUARE_OFF
            self.account.order_from_position(position)
            del position

    def strategy(self):
        """
        Actual manager implementation with the golden rules
        :return:
        """
        # Check for Exit
        if self.account.mtm + self.account.profit >= self.EXIT_PROFIT:
            self.exit()

        # Adjustment
        ratio = self.call.security.ltp / self.put.security.ltp
        square_off_leg = self.call if self.call.security.ltp < self.put.security.ltp else self.put
        reference_leg = self.put if self.call.security.ltp < self.put.security.ltp else self.call
        if ratio > self.RATIO or ratio < (1 / self.RATIO):
            # Trigger adjustment
            adjusted_position = self.adjust(square_off_leg, reference_leg)
            if ratio > self.RATIO:
                self.put = adjusted_position
            else:
                self.call = adjusted_position

    def end_strategy(self) -> None:
        """
        Graciously closes the manager based on the trigger
        :return:
        """
        pass
