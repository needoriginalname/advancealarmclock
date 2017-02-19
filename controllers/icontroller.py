import abc
from abc import ABCMeta, abstractmethod


class IController(metaclass=ABCMeta):

    @abstractmethod
    def update(self):
        # updates the controller's back end, sets the has_changed_config result to false
        pass

    @abstractmethod
    def has_changed_config(self):
        # returns if it has changed config this cycle
        pass
