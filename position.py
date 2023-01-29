from security import Security
from enum import Enum

class PositionTypes(int, Enum):
    """
    Enumeration class that handles the quantity multiplier
    """
    BUY = 1
    SELL = -1
    SQUARE_OFF = 0

class Position:
    """
    Class to define a position
    """

    def __init__(self):
        self.security: Security
        self.type: PositionTypes
        self.quantity: int

    def create_position(self, ):

    # TODO: To be implemented as necessary
