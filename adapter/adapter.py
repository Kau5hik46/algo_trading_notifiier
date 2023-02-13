from hashlib import md5
from typing import List, Dict

import requests

from entity.underlying_symbols import Symbol


class NSEAdapter:
    """
    Class to work with the NSE website to fetch live market data
    """

    API_URL = 'https://www.nseindia.com/api'

    def __init__(self, symbol: Symbol) -> None:
        self.session = requests.Session()
        self.records: dict = dict()
        self.set_symbol(symbol)

    def set_endpoint(self, endpoint: str) -> str:
        self.endpoint = endpoint
        self.url = NSEAdapter.API_URL + self.endpoint
        return self.url

    def set_symbol(self, symbol: Symbol) -> Symbol:
        self.symbol = symbol
        return self.symbol

    def _get_headers(self) -> dict:
        headers = {
            'User-Agent': md5(b'987654321').__str__()
        }
        return headers

    def _get_url_params(self) -> dict:
        params = dict()
        params['symbol'] = self.symbol
        return params

    def get_data(self, endpoint: str = '/option-chain-indices') -> Dict:
        self.set_endpoint(endpoint)
        headers = self._get_headers()
        params = self._get_url_params()
        response = self.session.get(self.set_endpoint(endpoint), headers=headers, params=params)
        return response.json()

    def get_expiries(self, endpoint: str = '/option-chain-indices') -> List:
        response = self.get_data(endpoint)
        print(response)
        return response['records']['expiryDates']

    def get_option(self, identifier: str = "") -> dict:
        """
        Parameters
        identifier: string attributed to the option
        :return: dict having the parameters for the option creation
        """
        sym = self.set_symbol(Symbol.BANK_NIFTY)
        if identifier == 'OPTIDXBANKNIFTY16-02-2023CE43000.00':
            return dict(
                {
                    "identifier": 'OPTIDXBANKNIFTY16-02-2023CE43000.00',
                    "underlying": sym,
                    "expiry_date": '16-Feb-2023',
                    "option_type": 'CE',
                    "strike_price": 43000,
                    "ltp": 190
                }
            )
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
        sym = self.set_symbol(Symbol.BANK_NIFTY)
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
    print(market.get_data())


if __name__ == '__main__':
    main()
