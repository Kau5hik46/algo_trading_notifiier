from typing import List

from design_patterns import Observer


class Publisher:
    """
    Class that publishes changes to the subscribers/observers
    """

    def __init__(self):
        """
        Initializer method
        """
        self.observers: List[Observer] = list()

    def subscribe(self, observer: Observer) -> None:
        """
        Method to subscribe an observer to the publisher
        Parameters
        ----------
        observer

        Returns
        -------

        """

    def _push(self):
        """
        method to push the changes to the the observers
        Returns
        -------

        """
        for observer in observers:
            observer.update()

    def __del__(self):
        LOGGER.info()