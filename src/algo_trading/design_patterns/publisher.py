import pandas as pd
from typing import List


from algo_trading.design_patterns.observer import Observer
from algo_trading import LOGGER


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
        observer: the observer object to subscribe

        Returns
        -------
        None
        """
        self.observers.append(observer)

    def _push(self):
        """
        method to push the changes to the observers

        Returns
        -------
        None
        """
        for observer in self.observers:
            observer.update()

    def unsubscribe(self, observer: Observer):
        """
        Method to unsubscribe the given Observer from the publisher
        Parameters
        ----------
        observer: The observer to be removed from the list of observers

        Returns
        -------

        """
        self.observers.remove(observer)

    def __del__(self):
        LOGGER.debug("{} has been deleted".format(self.__repr__()))