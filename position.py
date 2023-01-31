from enum import Enum

from security import Security


class PositionSides(int, Enum):
    """
    Enumeration class that handles the quantity multiplier
    """
    BUY = 1
    SELL = -1
    SQUARE_OFF = 0


class PositionDirections(str, Enum):
    """
    Enumeration class to determine the direction of the position
    """
    LONG = "LONG"
    SHORT = "SHORT"


class Position:
    """
    Class to define a position
    """

    def __init__(self, security: Security = None, side: PositionSides = None,
                 direction: PositionDirections = None, quantity: int = 0):
        if security is None or side is None or direction is None or quantity is 0:
            return
        self.security: Security = security
        self.side: PositionSides = side
        self.direction: PositionDirections = direction
        self.quantity: int = quantity

    # TODO: To be implemented as necessary
