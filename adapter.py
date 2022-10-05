from email import header
import imp
import json
from enum import Enum
from hashlib import md5
from select import select
import requests

class Symbol(str, Enum):
    NIFTY = 'NIFTY'
    BANK_NIFTY = 'BANKNIFTY'

params = {'symbol': Symbol.BANK_NIFTY}


session = requests.Session()
response = session.get(url, headers=headers, params=params)
print(response)
option_chain = response.json()
# print(json.dumps(option_chain, indent=4))
print(type(option_chain['records']['expiryDates'][0]))
print(option_chain['records']['expiryDates'])


class NSEAdapter():
    """
    Class to work with the NSE website to fetch live market data
    """
    
    API_URL = 'https://www.nseindia.com/api'
    
    def __init__(self, symbol: Symbol) -> None:
        self.session = requests.Session()
        
    def set_endpoint(self, endpoint: str) -> str:
        self.endpoint = endpoint
        self.url = NSEAdapter.API_URL + self.endpoint
        return self.url
        
    def set_symbol(self, symbol: Symbol) -> Symbol:
        self.symbol = symbol
        return self.symbol
        
    def _get_headers(self) -> dict:
        from random import random
        n = random()
        headers = {
            'User-Agent': md5(n).__str__()
        }
        return headers
    
    def _get_url_params(self) -> dict:
        params = dict()
        params['symbol'] = self.symbol
        return params
        
    def get_data(self, endpoint: str = '/option-chain-indices') -> dict:
        headers = self._get_headers()
        params = self._get_url_params()
        response = self.session.get(self.set_endpoint(endpoint), headers=headers, params=params)
        return response.json()
    
    