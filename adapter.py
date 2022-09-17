import json
from enum import Enum
from hashlib import md5
import requests

headers = {
    'User-Agent': md5(b'whatever').__str__()
}
url = 'https://www.nseindia.com/api/option-chain-indices'


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
