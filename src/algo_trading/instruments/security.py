from algo_trading.adapter.adapter import NSEAdapter
from algo_trading.design_patterns.observer import Observer


class Security(Observer):
    """
    Virtual class that abstracts all financial instruments: Stocks, Options, etc
    """

    def __init__(self, adapter: NSEAdapter):
        super().__init__(adapter)
        self.subscribe()
        self._ltp: float = 0
        self.__lot_size__: int = 0

    def __hash__(self):
        return hash("Security@{}".format(self.__repr__()))

    def __eq__(self, other):
        pass

    @property
    def ltp(self) -> float:
        """
        Method to get the last traded price of the given security

        :return:
            ltp(float): The last traded price upto 2 decimals
        """
        return self._ltp

    @ltp.setter
    def ltp(self, new_ltp: float):
        # TODO: Validate the new ltp
        self._ltp = new_ltp

    def update(self) -> None:
        """
        Method to update the changes from the API using adapter
        :return:
            None
        """
        pass
