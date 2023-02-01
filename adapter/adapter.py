from hashlib import md5

import requests

from entity.underlying_symbols import Symbol


class NSEAdapter:
    """
    Class to work with the NSE website to fetch live market data
    """

    API_URL = 'https://www.nseindia.com/api'

    def __init__(self, symbol: Symbol) -> None:
        self.session = requests.Session()
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
            'User-Agent': md5(b'123456789').__str__()
        }
        return headers

    def _get_url_params(self) -> dict:
        params = dict()
        params['symbol'] = self.symbol
        return params

    def get_data(self, endpoint: str = '/option-chain-indices') -> dict:
        self.set_endpoint(endpoint)
        headers = self._get_headers()
        params = self._get_url_params()
        response = self.session.get(self.set_endpoint(endpoint), headers=headers, params=params)
        return response.json()

    def get_option(self, underlying=None, expiry_date=None, option_type=None, strike_price=None, ltp=None) -> dict:
        """

        :return: dict having the parameters for the option creation
        """
        pass


def main():
    market = NSEAdapter(Symbol.BANK_NIFTY)
    print(market.get_data())


if __name__ == '__main__':
    main()
