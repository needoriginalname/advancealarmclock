import pyowm
import time

from controllers.icontroller import IController

WEATHER = 'Weather'
API_KEY = 'api-key'
LOCATION_CODE = 'location-code'
UPDATE_TIME = 'update-time'
MAX_NUMBER_OF_DAYS = 5


class WeatherController(IController):
    def has_changed_config(self):
        return self._config_changed

    def __init__(self, config):
        self.config = config[WEATHER]
        self.owm = pyowm.OWM(self.config[API_KEY])
        self.loc = self.config[LOCATION_CODE]
        self.time_to_check = int(self.config[UPDATE_TIME])
        self._time_last_checked = -1
        self.currentWeather = None
        self.weatherForecasts = None
        self.update()
        self._config_changed = False

    def update(self):
        if self._time_last_checked + self.time_to_check <= time.time():
            self._time_last_checked = time.time()
            self.currentWeather = self.owm.weather_at_place(self.loc).get_weather()
            self.weatherForecasts = self.owm.daily_forecast(self.loc, limit=MAX_NUMBER_OF_DAYS)

    def get_current_weather(self):
        return self.currentWeather

    def get_forecast_weathers(self):
        return self.weatherForecasts





