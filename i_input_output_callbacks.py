from abc import ABCMeta, abstractmethod

class IInputOutputCallbacks(metaclass = ABCMeta):

    def __init__(self):
        super(IInputOutputCallbacks, self).__init__()
    @abstractmethod
    def set_output(self, output_list):
        """Sets the string that should be displayed
        Keyword arguments:
        outputList -- a list of no more then 2 strings, to be displayed
        """
        pass
    @abstractmethod
    def get_buttons_pressed(self):
        """returns a list of EnumButton that just got pressed"""
        pass

    @abstractmethod
    def get_buttons_held_down(self):
        """returns a list of EnumButtons that are currently pressed down"""
        pass
