from tkwindow import TKWIndow
from configparser import ConfigParser
from tkwindow import TKWIndow
from controllers.weathercontroller import WeatherController

from controllers.alarmcontroller import AlarmController
from panels.timepanel import TimePanel
from panels.weatherpanel import WeatherPanel
from enumbutton import EnumButton
import os.path as path
import sys

FILE = "alarmclock.cfg"

class AlarmClock:
    def setup_config_parser(self):
        config = ConfigParser()
        config.read(FILE)
        return config

    def __init__(self):
        config = self.setup_config_parser()

        weather_controller = WeatherController(config)
        alarm_controller = AlarmController(config)
        pydora_controller = None

        self.controllers = [weather_controller, alarm_controller]

        weather_panel = WeatherPanel(config, weather_controller)
        time_panel = TimePanel(config, alarm_controller)
        pydora_panel = None

        if sys.platform.startswith('linux'):
            from controllers.pydoracontroller import PydoraController
            pydora_controller = PydoraController(config)
            self.controllers.append(pydora_controller)
            # TODO: add pydora panel here
        else:
            print("Non-Linux system found, skipping Pydora setup")

        self.gui_interface = TKWIndow(config, self)

        self.panels = [time_panel, weather_panel]
        if pydora_panel is not None:
            self.panels.append(pydora_panel)
        self.panel_index = 0;

    def start(self):
        self.gui_interface.start()

    def update(self):
        keys_pressed = self.gui_interface.get_buttons_pressed()
        keys_held = self.gui_interface.get_buttons_held_down()
        if not self.panels[self.panel_index].process_keys(keys_pressed, keys_held):
            if EnumButton.LEFT in keys_pressed:
                self.panel_index = self._wrap(self.panel_index - 1, 0, len(self.panels) - 1)
            elif EnumButton.RIGHT in keys_pressed:
                self.panel_index = self._wrap(self.panel_index + 1, 0, len(self.panels) - 1)


        for controller in self.controllers:
            controller.update()
        self.gui_interface.set_output(self.panels[self.panel_index].get_display())

    def _wrap(self, n, min_value, max_value):
        if n > max_value:
            n = (n - max_value) + min_value

        if n < min_value:
            n = max_value - (min_value - n)

        return n






if __name__ == "__main__":
    ac = AlarmClock()
    ac.start()


