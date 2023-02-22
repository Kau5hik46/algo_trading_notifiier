import json
import time
from datetime import datetime
from hashlib import md5
from typing import List, Dict

import pandas as pd
import requests

from algo_trading.constants import DATE_FORMAT, DATE_FORMAT_OPTID
from algo_trading.design_patterns.publisher import Publisher
from algo_trading.entity.underlying_symbols import Symbol
from algo_trading.exceptions.adapter_exceptions import OptionNotFoundError


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
        """
        The get_data method retrieves data from an external source and stores it in the records member of the class
        instance. It also pushes any changes to the observers subscribed to the instance.

        Parameters:
            None
        Returns:
            A dictionary containing the retrieved data.
        Raises:
            None
        """
        # Getting the data and storing in the records member
        headers = self._get_headers()
        params = self._get_url_params()
        response = self.session.get(self.url, headers=headers, params=params)
        self.records = response.json()['records']

        # Pushing the changes to the consuming observers
        self._push()

        return self.records

    def get_expiries(self) -> List:
        """
        Retrieves the expiry dates for a financial instrument.

        Sends a GET request to retrieve data from an API endpoint, and returns a list of expiry dates for a given
        financial instrument.
        The response is expected to be in JSON format with a 'records' key containing an 'expiryDates' value.

        Returns:
            List: A list of expiry dates in string format.

        Raises:
            Exception: If the GET request fails or if the response is not in the expected format.
        """
        response = self.get_data()
        print(response)
        return response['records']['expiryDates']

    @staticmethod
    def _parse_option_identifier(option_id: str):
        """
        Parses an option identifier string into its component parts.
        :param option_id: The option identifier string (e.g. "OPTIDXNIFTY29-06-2023CE9500.00").
        :return: A tuple containing the symbol, expiry date, option type, and strike price.
        """
        symbol = ''
        expiry_date = ''
        option_type = ''
        strike_price = 0.0

        # Extract symbol and expiry date
        if 'NIFTY' in option_id:
            symbol = Symbol.NIFTY
        if 'BANKNIFTY' in option_id:
            symbol = Symbol.BANK_NIFTY
        else:
            return None  # Invalid option identifier

        if symbol == Symbol.BANK_NIFTY:
            option_prefix = 'OPTIDXBANKNIFTY'
        elif symbol == Symbol.NIFTY:
            option_prefix = 'OPTIDXNIFTY'
        else:
            raise NotImplementedError

        prefix_len = len(option_prefix)

        if option_id.startswith(option_prefix):
            expiry_start = prefix_len
            expiry_end = prefix_len + 10
            expiry_date = option_id[expiry_start:expiry_end]
            expiry_date = f"{expiry_date[:2]}-{expiry_date[3:5]}-{expiry_date[-4:]}"
            expiry_date = datetime.strftime(datetime.strptime(expiry_date, DATE_FORMAT_OPTID).date(), DATE_FORMAT)

            # Extract option type and strike price
            option_type = option_id[expiry_end:expiry_end + 2]
            strike_price = float(option_id[expiry_end + 2:])
        else:
            raise ValueError(
                'Invalid Option Identifier: {}, {}'.format(option_id, option_prefix))  # Invalid option identifier

        return (symbol, expiry_date, option_type, strike_price)

    def get_option_data(self, identifier: str = ""):
        """
        Returns the option chain data for the specified option identifier.
        :param identifier: The option identifier string (e.g. "OPTIDXNIFTY29-06-2023CE9500.00").
        :return: The option chain data for the specified option as a dictionary.
        """

        symbol, expiry_date, option_type, strike_price = self._parse_option_identifier(option_id=identifier)
        print(self._parse_option_identifier(option_id=identifier))
        filtered_data = [data for data in self.records['data'] if data['strikePrice'] == strike_price
                         and data['expiryDate'] == expiry_date]

        # If the option was not found, raise OptionNotFoundError
        if not filtered_data:
            raise OptionNotFoundError(identifier, "Filtered data empty")

        return filtered_data[0][option_type]

    def get_option_by_ltp(self, ltp: float, option_type: str, expiry_date: str) -> Dict:
        """

        Parameters
        ----------
        expiry_date: expiry date as string for the requested option
        option_type: Call or put
        ltp: float value of the last price for which the search happens.

        Returns
        -------
        Dict: dictionary of parameters required to create the option
        """
        data = self.records['data']

        # Filter the option chain data based on the expiry date and option type
        filtered_data = [d for d in data if d['expiryDate'] == expiry_date and d['optionType'] == option_type]

        if not filtered_data:
            raise ValueError('No options found for the given expiry date and option type')

        # Find the option that is closest to the given last price
        closest_option = None
        min_price_diff = float('inf')
        for option in filtered_data:
            price_diff = abs(option['strikePrice'] - ltp)
            if price_diff < min_price_diff:
                min_price_diff = price_diff
                closest_option = option

        return closest_option


def main():
    market = NSEAdapter(Symbol.BANK_NIFTY)

    for i in range(0, 60, 5):
        market.get_data()
        print(market.get_option_data('OPTIDXBANKNIFTY23-02-2023CE39900.00')['lastPrice'])
        time.sleep(5)


if __name__ == '__main__':
    main()
