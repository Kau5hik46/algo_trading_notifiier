import json
import time
from hashlib import md5
from typing import List, Dict

import pandas as pd
import requests

from algo_trading.design_patterns.publisher import Publisher
from algo_trading.entity.underlying_symbols import Symbol


class NSEAdapter(Publisher):
    """
    Class to work with the NSE website to fetch live market data
    """

    API_URL = 'https://www.nseindia.com/api'

    def __init__(self, symbol: Symbol) -> None:
        super().__init__()
        self._symbol: Symbol = symbol
        self._endpoint: str = '/option-chain-indices'
        self._url: str = NSEAdapter.API_URL + self._endpoint
        self.session: requests.Session = requests.Session()
        self.records: dict = dict()

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint: str):
        self._endpoint = endpoint

    @property
    def url(self) -> str:
        self._url = NSEAdapter.API_URL + self.endpoint
        return self._url

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    @staticmethod
    def _get_headers() -> dict:
        headers = {
            'User-Agent': md5(b'987654321').__str__()
        }
        return headers

    def _get_url_params(self) -> dict:
        params = dict()
        params['symbol'] = self.symbol
        return params

    def get_data(self) -> Dict:
        # Getting the data and storing in the records member
        headers = self._get_headers()
        params = self._get_url_params()
        response = self.session.get(self.url, headers=headers, params=params)
        self.records = response.json()

        # Pushing the changes to the consuming observers
        self._push()

        return self.records

    def get_expiries(self) -> List:
        response = self.get_data()
        print(response)
        return response['records']['expiryDates']

    def get_option(self, identifier: str = "") -> dict:
        """
        Parameters
        identifier: string attributed to the option
        :return: dict having the parameters for the option creation
        """
        sym = self.symbol
        if identifier == 'OPTIDXBANKNIFTY16-02-2023CE43000.00':
            return self.records['records']['data']
        if identifier == 'OPTIDXBANKNIFTY16-02-2023PE41000.00':
            return dict(
                {
                    "identifier": 'OPTIDXBANKNIFTY16-02-2023PE41000.00',
                    "underlying": sym,
                    "expiry_date": '16-Feb-2023',
                    "option_type": 'CE',
                    "strike_price": 43000,
                    "ltp": 80
                }
            )

    def get_option_by_ltp(self, ltp: float, option_type: str) -> Dict:
        """

        Parameters
        ----------
        option_type: Call or put
        ltp: float value of the last price for which the search happens.

        Returns
        -------
        Dict: dictionary of parameters required to create the option
        """
        sym = self.symbol
        if option_type == "CE":
            return dict(
                {
                    "identifier": 'OPTIDXBANKNIFTY16-02-2023CE43000.00',
                    "underlying": sym,
                    "expiry_date": '16-Feb-2023',
                    "option_type": 'CE',
                    "strike_price": 43000,
                    "ltp": 120
                }
            )
        if option_type == "PE":
            return dict(
                {
                    "identifier": 'OPTIDXBANKNIFTY16-02-2023PE41000.00',
                    "underlying": sym,
                    "expiry_date": '16-Feb-2023',
                    "option_type": 'PE',
                    "strike_price": 41000,
                    "ltp": 120
                }
            )


def main():
    market = NSEAdapter(Symbol.BANK_NIFTY)

    for i in range(5):
        market.get_data()
        print(market.get_option('OPTIDXBANKNIFTY16-02-2023CE43000.00'))
        time.sleep(1)


if __name__ == '__main__':
    main()
