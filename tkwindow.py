from tkinter import *
from tkinter import ttk
from i_input_output_callbacks import IInputOutputCallbacks
from enumbutton import EnumButton


class TKWIndow():
    """
    A gui for the Advance Alarm Clock program. This is intended for testing the
     internal progarmming without the needed display physical hardware.
    """
    

    def button_press(self, event):
        button = EnumButton.get_button_from_keyboard(event.char)
        self.buttons_pressed.append(button)
        self.buttons_held_down.append(button)
        
    def button_release(self, event):
        button =  EnumButton.get_button_from_keyboard(event.char)
        for i in range(self.buttons_held_down.count(button)):
            self.buttons_held_down.remove(button)

    def get_buttons_held_down():
        return self.buttons_held_down

    def get_buttons_pressed():
        return self.buttons_pressed

    def set_output(self, output_list):
        if len(output_list) == 1:
            self.output1.set(output_list[0])
            self.output2.set("")
        elif len(output_list) >= 2:
            self.output1.set(output_list[0])
            self.output2.set(output_list[1])
        else:
            self.output1.set("")
            self.output2.set("")
            
    def __init__(self):
        self.root = Tk()
        self.root.title("Advance Alarm Clock")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid()

        self.button_down_string = StringVar()
        self.output1 = StringVar()
        self.output2 = StringVar()

        ttk.Label(self.mainframe, textvariable=self.button_down_string).grid()
        ttk.Label(self.mainframe, textvariable=self.output1).grid()
        ttk.Label(self.mainframe, textvariable=self.output2).grid()

        self.buttons_pressed = []
        self.buttons_held_down = []
        self.root.bind("<KeyPress>", lambda e: self.button_press(e))
        self.root.bind("<KeyRelease>", lambda e: self.button_release(e))


if __name__ == '__main__':
    t = TKWIndow()
    t.output1.set("Test")
