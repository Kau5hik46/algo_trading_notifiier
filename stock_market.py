class Option():
    """
    Entity that provides methods to work with a specific option
    """

    def __init__(self, strike, expiry, direction):
        self.strike = strike
        self.expiry = expiry
        self.direction = direction


#   Needs more methods to simplify the usage.

class OptionChain():
    """
    Interface to work with option chain data fetched from NSE
    """

    def __init__(self, raw_data):
        self.data = raw_data

# Need more methods to work with the whole option chain data
