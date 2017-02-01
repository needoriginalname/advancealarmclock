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
        d = ["",""]
        topleft = None
        topright = None
        bottomleft = None
        bottomright = None
        lcd = None
        if self._panel_index == 0:
            current_weather = self.weather_controller.get_current_weather()
            temps = current_weather.get_temperature(self.weather_config[UNIT])

            topleft = datetime.now().strftime(self.config[TIME_FORMAT])
            topright = str(temps[TEMP])
            bottomleft = current_weather.get_detailed_status()
            bottomright = ""

            lcd = LCDDisplayDesigner(top_left= topleft, top_right=topright,bottom_left=bottomleft,
                                     bottom_right=bottomright)
        else:
            forcaster = self.weather_controller.get_forecast_weathers().get_forecast()
            forcast_weather = forcaster.get(self._panel_index - 1)
            time = datetime.fromtimestamp(forcast_weather.get_reference_time())
            temps = forcast_weather.get_temperature(self.weather_config[UNIT])

            topleft = time.strftime(self.config[DATE_FORMAT])
            topright = str(temps[MIN]) + " / " + str(temps[MAX])
            bottomleft = forcast_weather.get_detailed_status()
            bottomright = ""  # temps["morn"] + " / " + temps["day"] + " / " + temps["eve"]
            lcd = LCDDisplayDesigner(top_left=topleft, top_right=topright, bottom_left=bottomleft,
                                     bottom_right=bottomright)


        return lcd

    def __init__(self, config, weather_controller):
        self.config = config[GENERAL]
        self.weather_config = config[WEATHER]
        self.weather_controller = weather_controller
        self._panel_index = 0

@staticmethod
def _get_center_padding(s):
    # get padding to center the string for middle of display
    n = 20 - len(s)
    l = math.floor(n / 2)
    r = math.ceil(n / 2)

    if l < 0:
        l = 0
    if r < 0:
        r = 0

    return l, r

def _center_string(self, s):
    l, r = self._get_center_padding(s)
    result = " " * l + s + " " * r
    return result