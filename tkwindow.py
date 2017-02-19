from tkinter import *
from tkinter import ttk
from i_input_output_callbacks import IInputOutputCallbacks
from enumbutton import EnumButton


class TKWIndow(IInputOutputCallbacks):
    """
    A gui for the Advance Alarm Clock program. This is intended for testing the
     internal progarmming without the needed display physical hardware.
    """

    def update(self):
        self.button_down_string = str(self.buttons_held_down)
        self.button_press_string = str(self.buttons_pressed)
        # print("pressed " + str(self.buttons_pressed))
        # print("down " + str(self.buttons_held_down))

    def button_press(self, event):
        button = EnumButton.get_button_from_keyboard(event.char)
        if button not in self.buttons_pressed and button not in self.buttons_held_down:
            self.buttons_pressed.append(button)
            self.buttons_held_down.append(button)
        elif button in self.buttons_held_down:
            pass

    def button_release(self, event):
        button = EnumButton.get_button_from_keyboard(event.char)
        for i in range(self.buttons_held_down.count(button)):
            self.buttons_held_down.remove(button)

    def get_buttons_held_down(self):
        return self.buttons_held_down

    def get_buttons_pressed(self):
        return self.buttons_pressed

    def set_output(self, output_list):
        self.output1.set(output_list[0])
        self.output2.set(output_list[1])

    def __init__(self, config, alarm_clock_head):
        self.root = Tk()
        self.root.title("Advance Alarm Clock")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid()
        self.config = config

        self.button_press_string = StringVar()
        self.button_down_string = StringVar()
        self.output1 = StringVar()
        self.output2 = StringVar()

        ttk.Label(self.mainframe, textvariable=self.button_press_string).grid()
        ttk.Label(self.mainframe, textvariable=self.button_down_string).grid()
        ttk.Label(self.mainframe, textvariable=self.output1).grid()
        ttk.Label(self.mainframe, textvariable=self.output2).grid()

        self.buttons_pressed = []
        self.buttons_held_down = []
        self.root.bind("<KeyPress>", lambda e: self.button_press(e))
        self.root.bind("<KeyRelease>", lambda e: self.button_release(e))
        self.alarm_clock_head = alarm_clock_head

    def start(self):
        self.root.after(100, func=self._loop)
        self.root.mainloop()

    def _loop(self):
        self.update()
        self.alarm_clock_head.update()
        self.buttons_pressed.clear()
        self.root.after(100, func=self._loop)
