from enum import Enum


class PositionSide(int, Enum):
    """
    Enumeration class that handles the quantity multiplier
    """
    BUY = 1
    SELL = -1
    SQUARE_OFF = 0


class PositionDirection(str, Enum):
    """
    Enumeration class to determine the direction of the position
    """
    LONG = "LONG"
    SHORT = "SHORT"
