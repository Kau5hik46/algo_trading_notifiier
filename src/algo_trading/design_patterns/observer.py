from algo_trading import LOGGER


class Observer:
    """
    Observer virtual class that has abstract methods to perform subscribe, update and delete operations
    """
    def __init__(self, publisher):
        """
        Initializer method
        """
        self.publisher = publisher

    def subscribe(self):
        """
        Method to subscribe to the given publisher

        Returns:
        -------
        None
        """
        self.publisher.subscribe(self)

    def update(self):
        """
        Changes the state of the observer based on the input given from the publisher

        Returns
        -------
        None
        """
        # To process it as required
        pass

    def _unsubscribe(self):
        self.publisher.unsubscribe(self)
        self.publisher = None

    def __del__(self):
        self._unsubscribe()
        LOGGER.debug("{} object is deleted".format(self.__repr__()))
