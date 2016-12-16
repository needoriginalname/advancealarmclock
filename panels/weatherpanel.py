from panels.ipanel import IPanel
from enum import Enum
from enumbutton import EnumButton
from datetime import datetime
MAX_PANELS = 5
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
        d = ["",""]
        topleft = None
        topright = None
        bottomleft = None
        bottomright = None
        if self._panel_index == 0:
            current_weather = self.weather_controller.get_current_weather()
            temps = current_weather.get_temperature(self.weather_config[UNIT])

            topleft = datetime.now().strftime(self.config[TIME_FORMAT])
            topright = str(temps[TEMP_MIN]) + " / " + str(temps[TEMP_MAX])
            bottomleft = current_weather.get_detailed_status()
            bottomright = str(temps[TEMP])
        else:
            forcaster = self.weather_controller.get_forecast_weathers().get_forecast()
            forcast_weather = forcaster.get(self._panel_index - 1)
            time = datetime.fromtimestamp(forcast_weather.get_reference_time())
            temps = forcast_weather.get_temperature(self.weather_config[UNIT])

            topleft = time.strftime(self.config[DATE_FORMAT])
            topright = str(temps[MIN]) + " / " + str(temps[MAX])
            bottomleft = forcast_weather.get_detailed_status()
            bottomright = ""  # temps["morn"] + " / " + temps["day"] + " / " + temps["eve"]

        space1 = 20 - (len(topleft) + len(topright))
        space2 = 20 - (len(bottomleft) + len(bottomright))
        if (space1 < 0):
            space1 = 1
        if (space2 < 0):
            space2 = 1
        output1 = topleft + (" " * space1) + topright
        output2 = bottomleft + (" " * space2) + bottomright

        d[0] = output1
        d[1] = output2

        return d

    def __init__(self, config, weather_controller):
        self.config = config[GENERAL]
        self.weather_config = config[WEATHER]
        self.weather_controller = weather_controller
        self._panel_index = 0
