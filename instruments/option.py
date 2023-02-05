from datetime import date, datetime

from entity.underlying_symbols import Symbol
from adapter.adapter import NSEAdapter
from constants import DATE_FORMAT
from instruments.security import Security


class Option(Security):
    """
    Class to abstract the option security
    """

    def __init__(self, underlying: Symbol, expiry_date: str, ) -> None:
        super().__init__()
        self.expiry_date: date = datetime.strptime(expiry_date, DATE_FORMAT).date()
        self.underlying: Symbol = Symbol.BANK_NIFTY
        self.strike_price: int = 42000
        self.option_type: str = "CE"

    def __repr__(self):
        exp = self.expiry_date.strftime("%d-%m-%Y")
        return "{} {} {} {}".format(self.underlying, self.strike_price, self.option_type, exp)

    def __update__(self, adapter: NSEAdapter) -> None:
        updated_values = adapter.get_option(
            underlying=self.underlying,
            strike_price=self.strike_price,
            expiry_date=self.expiry_date,
            option_type=self.option_type
        )
        self.ltp = updated_values['ltp']