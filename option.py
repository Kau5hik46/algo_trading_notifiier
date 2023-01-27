from datetime import date

from adapter import NSEAdapter, Symbol
from security import Security


class Option(Security):
    """
    Class to abstract the option security
    """

    def __init__(self, adapter: NSEAdapter) -> None:
        super().__init__(adapter)
        self._expiry: date = date.today()
        self.underlying: Symbol = Symbol.BANK_NIFTY
        self.strike_price: int = 42000
        self.option: str = "CE"

    def __repr__(self):
        exp = self.expiry.strftime("%d-%m-%Y")
        return "{} {} {} {}".format(self.underlying, self.strike_price, self.option, exp)

    @property
    def expiry(self) -> date:
        return self._expiry

    @expiry.setter
    def expiry(self, exp: date):
        # TODO: Implement a check for valid expiry
        self._expiry = exp
