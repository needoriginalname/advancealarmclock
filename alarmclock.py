from panels.pandorapanel import PandoraPanel
from tkwindow import TKWIndow
from configparser import ConfigParser
from tkwindow import TKWIndow
from controllers.weathercontroller import WeatherController

from controllers.alarmcontroller import AlarmController
from controllers.pydoracontroller import PydoraController
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
        self.config = self.setup_config_parser()

        weather_controller = WeatherController(self.config)
        alarm_controller = AlarmController(self.config)
        pydora_controller = PydoraController(self.config)

        self.controllers = [weather_controller, alarm_controller, pydora_controller]

        weather_panel = WeatherPanel(self.config, weather_controller)
        time_panel = TimePanel(self.config, alarm_controller)
        pydora_panel = PandoraPanel(self.config, pydora_controller)

        self.gui_interface = TKWIndow(self.config, self)

        self.panels = [time_panel, weather_panel, pydora_panel]

        self.panel_index = 0;

    def start(self):
        self.gui_interface.start()

    def update(self):
        keys_pressed = self.gui_interface.get_buttons_pressed()
        keys_held = self.gui_interface.get_buttons_held_down()
        if not self.panels[self.panel_index].process_keys(keys_pressed, keys_held):
            if EnumButton.LEFT in keys_pressed:
                self.panel_index = self._wrap(self.panel_index - 1, len(self.panels) - 1)
            elif EnumButton.RIGHT in keys_pressed:
                self.panel_index = self._wrap(self.panel_index + 1, len(self.panels) - 1)

        for controller in self.controllers:
            controller.update()
        self.gui_interface.set_output(self.panels[self.panel_index].get_display())

    @staticmethod
    def _wrap(n, max_value):
        if n > max_value:
            n = 0

        if n < 0:
            n = max_value

        return n


if __name__ == "__main__":
    ac = AlarmClock()
    ac.start()


