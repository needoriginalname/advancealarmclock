from abc import ABCMeta, abstractmethod


class IPanel(metaclass=ABCMeta):
    @abstractmethod
    def get_display(self):
        # gets the current display of the panel
        pass

    @abstractmethod
    def process_keys(self, keys_pressed, keys_down):
        """ processes the key strokes

        Keyword Arguments:
            keys_pressed    -- A list of keys that were just pressed
            keys_down       -- A list of keys that are currently down

        Returns:
            true -- if an operation was done on panel
            false -- otherwise
        """
        pass
