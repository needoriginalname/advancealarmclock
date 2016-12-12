import pyowm
import time

class WeatherController:
    def __init__(self, config):
        self.config = config['Weather']
        self.owm = pyowm.OWM(self.config['api-key'])
        self.loc = self.config['location-code']
        self.time_to_check = int(self.config['update-time'])
        self._time_last_checked = -1
        self.currentWeather = None
        self.weatherForecasts = None
        self.update()

    def update(self):
        if self._time_last_checked + self.time_to_check <= time.time():
            self._time_last_checked = time.time()
            self.currentWeather = self.owm.weather_at_place(self.loc).get_weather()
            self.weatherForecasts = self.owm.daily_forecast(self.loc, limit=3)

    def get_current_weather(self):
        return self.currentWeather

    def get_forecast_weathers(self):
        return self.weatherForecasts





