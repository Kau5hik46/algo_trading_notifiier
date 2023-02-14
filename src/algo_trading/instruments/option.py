from datetime import date, datetime

from algo_trading.entity.underlying_symbols import Symbol
from algo_trading.adapter.adapter import NSEAdapter
from algo_trading.constants import DATE_FORMAT
from algo_trading.instruments.security import Security


class Option(Security):
    """
    Class to abstract the option security
    """
    # TODO: implement check to get the same object every time it is created with the same parameters
    def __init__(self, adapter: NSEAdapter, identifier: str, underlying: Symbol, expiry_date: str, option_type: str,
                 strike_price: int, ltp: float) -> None:
        super().__init__(adapter)
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

    def update(self) -> None:
        """
        Concrete implementation of the update function that fetches the data from the adapter and updates accordingly
        Returns
        -------

        """
        updated_values = self.adapter.get_option(self.identifier)
        self.ltp = updated_values['ltp']