from panels.ipanel import IPanel
from enum import Enum
from enumbutton import EnumButton
from datetime import datetime
from .lcddisplaydesigner import LCDDisplayDesigner

MAX_PANELS = 3
DEGREE_SYMBOL = u"\u00b0"

GENERAL = "General"
WEATHER = "Weather"
UNIT = "unit"
TIME_FORMAT = "time-format"
DATE_FORMAT = "date-format"

# pyowm consts
TEMP_MIN = "temp_min"
TEMP_MAX = "temp_max"
TEMP = "temp"
MAX = "max"
MIN = "min"


class WeatherPanel(IPanel):
    def process_keys(self, keys_pressed, keys_down):
        if EnumButton.ENTER in keys_down:
            # ensures it always shows a forecast
            if self._panel_index == 0:
                self._panel_index = 1

            # toggles through the different forecasts
            if EnumButton.RIGHT in keys_pressed:
                self._panel_index += 1
            elif EnumButton.LEFT in keys_pressed:
                self._panel_index -= 1
            if self._panel_index > MAX_PANELS:
                self._panel_index = 1
            if self._panel_index < 1:
                self._panel_index = MAX_PANELS
            return True

        else:

            # display only the current weather panel
            self._panel_index = 0
            return False

    def get_display(self):
        d = ["", ""]
        if self._panel_index == 0:
            current_weather = self.weather_controller.get_current_weather()
            temps = current_weather.get_temperature(self.weather_config[UNIT])

            top_left = datetime.now().strftime(self.config[TIME_FORMAT])
            top_right = str(temps[TEMP])
            bottom_left = current_weather.get_detailed_status()
            bottom_right = ""

            lcd = LCDDisplayDesigner(top_left=top_left, top_right=top_right, bottom_left=bottom_left,
                                     bottom_right=bottom_right)
        else:
            forecaster = self.weather_controller.get_forecast_weathers().get_forecast()
            forecast_weather = forecaster.get(self._panel_index - 1)
            time = datetime.fromtimestamp(forecast_weather.get_reference_time())
            temps = forecast_weather.get_temperature(self.weather_config[UNIT])

            top_left = time.strftime(self.config[DATE_FORMAT])
            top_right = str(temps[MIN]) + " / " + str(temps[MAX])
            bottom_left = forecast_weather.get_detailed_status()
            bottom_right = ""  # temps["morn"] + " / " + temps["day"] + " / " + temps["eve"]
            lcd = LCDDisplayDesigner(top_left=top_left, top_right=top_right, bottom_left=bottom_left,
                                     bottom_right=bottom_right)

        return lcd

    def __init__(self, config, weather_controller):
        self.config = config[GENERAL]
        self.weather_config = config[WEATHER]
        self.weather_controller = weather_controller
        self._panel_index = 0
