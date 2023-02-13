from datetime import date, datetime

from entity.underlying_symbols import Symbol
from adapter.adapter import NSEAdapter
from constants import DATE_FORMAT
from instruments.security import Security


class Option(Security):
    """
    Class to abstract the option security
    """
    # TODO: implement check to get the same object every time it is created with the same parameters
    def __init__(self, identifier: str, underlying: Symbol, expiry_date: str, option_type: str, strike_price: int, ltp: float) -> None:
        super().__init__()
        self.identifier: str = identifier
        self.expiry_date: date = datetime.strptime(expiry_date, DATE_FORMAT).date()
        self.underlying: Symbol = underlying
        self.strike_price: int = strike_price
        self.option_type: str = option_type
        self.ltp = ltp

    def __hash__(self):
        return hash("Option@{}".format(self.__repr__()))

    def __repr__(self):
        return self.identifier

    def __str__(self):
        return "{}: {}".format(self.__repr__(), self.ltp)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.identifier == other.identifier
        else:
            return False

    def __update__(self, adapter: NSEAdapter) -> None:
        print(self.identifier)
        updated_values = adapter.get_option(self.identifier)
        self.ltp = updated_values['ltp']