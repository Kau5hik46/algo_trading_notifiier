from datetime import date, datetime

from adapter import Symbol
from constants import DATE_FORMAT
from security import Security


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
