from enum import Enum


class EnumButton(Enum):
    """Enum of buttons, that maps between keys and hardware buttons
    to software"""

    ENTER = ('s', "enter")
    SELECT = ('d', "select")
    RIGHT = ('f', "right")
    LEFT = ('a', "left")
    PLAY = ('w', "play")
    STOP = ('e', "stop")
    SKIP = ('r', "skip")

    def __init__(self, key, name):
        self._key = key
        self._name = name

    def __str__(self):
        return self._name

    def get_keyboard_key(self):
        return self._key

    @classmethod
    def get_button_from_keyboard(cls, key):
        # given keyboard key, returns the respective EnumButton
        for member in list(cls):
            if member.get_keyboard_key() == key:
                return member
        return None


if __name__ == "__main__":
    print(EnumButton.get_button_from_keyboard('z'))
