from instruments.security import Security


class Position:
    """
    Class to define a position
    """

    def __init__(self, security: Security = None, side: PositionSide = None,
                 direction: PositionDirection = None, quantity: int = 0):
        if security is None or side is None or direction is None or quantity == 0:
            return
        self.security: Security = security
        self.side: PositionSide = side
        self.direction: PositionDirection = direction
        self.quantity: int = quantity

    # TODO: To be implemented as necessary
