from enum import Enum
import requests
import uuid
from utilities import Datasaved
import utilities
import pandas as pd
import json 
import option 
from exceptions import LtpError

class Symbol(str, Enum):
    NIFTY = 'NIFTY'
    BANK_NIFTY = 'BANKNIFTY'

# params = {'symbol': Symbol.BANK_NIFTY}


# session = requests.Session()
# response = session.get(url, headers=headers, params=params)
# print(response)
# option_chain = response.json()
# print(type(option_chain['records']['expiryDates'][0]))
# print(option_chain['records']['expiryDates'])

class NSEAdapter():
    """
    Class to work with the NSE website to fetch live market data
    """
    #for symbol in [sym.value for sym in Symbol]:
     #   dict[symbol] = Datasaved(strike_price, expiry_date, ltp, underlying, expiry_dates)
    
    
    
    global_data_dict = dict.fromkeys([e.value for e in Symbol], pd.DataFrame())
    
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
        
    def get_headers(self) -> dict:
        headers = {
            'User-Agent': str(uuid.uuid4())
        }
        return headers
    
    def _get_url_params(self) -> dict:
        params = dict()
        params['symbol'] = self.symbol
        return params
        
    def get_data(self, endpoint: str = '/option-chain-indices') -> dict:
        response = self.session.get(self.set_endpoint(endpoint), headers=self.get_headers(), params=self._get_url_params())
        #NSEAdapter.global_data_dict[self.symbol] = response.json()
        df = pd.read_json(response.text)
        NSEAdapter.global_data_dict[self.symbol] = df
    
    def get_underlying_value(self, symbol):
        return NSEAdapter.global_data_dict[symbol]["underlyingValue"]["records"]
    
    def get_option(self, underlying, option_type, expiry_date, ltp=None, strike_price=None):
        response_dict = {"underlying": underlying, "option_type": option_type, "expiry_date": expiry_date, "strike_price": strike_price, "ltp": ltp}
        if (ltp is not None) and (strike_price is None):
            data_list =  NSEAdapter.global_data_dict[underlying]["data"]
            try:
                ltp = utilities.get_nearest_ltp(ltp, [temp_dict[option_type]["latestPrice"] for temp_dict in data_list if temp_dict["expiryDate"]==expiry_date])
            except ValueError as e:
                raise LtpError(e)
            response_dict["ltp"] = ltp
            response_dict["strike_price"] = [temp_dict[option_type]["strike_price"] for temp_dict in data_list if temp_dict["expiryDate"]==expiry_date and temp_dict["ltp"]==ltp][0]
            return response_dict
        elif (ltp is None) and (strike_price is not None):
            data_list =  NSEAdapter.global_data_dict[underlying]["data"]
            for temp_dict in data_list:
                if temp_dict["strikePrice"] == strike_price and temp_dict["expiryDate"] == expiry_date:
                    response_dict["ltp"] = temp_dict[option_type]["latestPrice"]  
                    return response_dict
        return response_dict
                
    
def main():
    market = NSEAdapter(Symbol.BANK_NIFTY)
    print(market.get_data())
    
if __name__ == '__main__':
    main()