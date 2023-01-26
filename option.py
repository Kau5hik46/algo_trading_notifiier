from datetime import date

from adapter import Adapter
from security import Security


class Option(Security):
    """
    Class to abstract the option security
    """
    def __init__(self, adapter: Adapter) -> None:
        super().__init__(adapter)
        self._expiry: date = date.today()
        self.

    def __repr__(self):

    @property
    def expiry(self) -> date:
        return self._expiry

    @expiry.setter
    def expiry(self, exp: date):
        #TODO: Implement a check for valid expiry
        self._expiry = exp

class Call(Option):
    def __init__(self) -> None:
        super().__init__()

class Put(Option):
    def __init__(self) -> None:
        super().__init__()


from typing import Optional, List
