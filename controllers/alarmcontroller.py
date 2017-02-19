import pygame
import datetime
import os

from controllers.icontroller import IController

ALARM_SECTION = "Alarm"
GENERAL = "General"
ALARM_FILE_LOCATION = "alarm.wav"
ALARM_ENABLED = "alarm-enabled"
HOUR = 'hour'
MINUTE = 'minute'
SNOOZE = 'snooze'


class AlarmController(IController):
    def has_changed_config(self):
        return self.changed_config

    def __init__(self, config):
        self.alarm_config = config[ALARM_SECTION]
        self.config = config[GENERAL]

        # setup the alarm sound
        sound_filepath = os.path.join(os.path.dirname(__file__), ALARM_FILE_LOCATION)
        pygame.mixer.init()

        self.sound_file = pygame.mixer.music.load(sound_filepath)

        self._is_alarm_enabled = self.alarm_config[ALARM_ENABLED]
        self.audio_playing = None

        # sets the alarm time
        self.alarm_time = None
        self._is_alarm_on = False
        self.set_alarm_time(int(self.alarm_config[HOUR]), int(self.alarm_config[MINUTE]))
        self.snooze_time = int(self.alarm_config[SNOOZE])
        self.changed_config = False

    def turn_off_alarm(self):
        self._is_alarm_on = False

    def reset_alarm_from_configs(self):
        self.turn_off_alarm()
        self.set_alarm_time(self.alarm_config[HOUR], self.alarm_config[MINUTE])

    def snooze(self):
        time_now = datetime.datetime.now().replace(second=0, microsecond=0)
        time_snooze = time_now + datetime.timedelta(minutes=self.snooze_time)

        self.set_alarm_time(time_snooze.hour, time_snooze.minute)

    def add_hour_to_alarm_config(self, reverse=False):
        alarm_hour = int(self.alarm_config[HOUR])
        alarm_min = int(self.alarm_config[MINUTE])
        d = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_min, second=0, microsecond=0)
        hours_to_change = 1
        if reverse:
            hours_to_change = -1
        d = d + datetime.timedelta(hours=hours_to_change)
        self.alarm_config[HOUR] = str(d.hour)
        self.alarm_config[MINUTE] = str(d.minute)
        self.set_alarm_time(d.hour, d.minute)
        self.changed_config = True

    def add_minute_to_alarm_config(self, reverse=False):
        alarm_hour = int(self.alarm_config[HOUR])
        alarm_min = int(self.alarm_config[MINUTE])
        d = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_min, second=0, microsecond=0)
        minutess_to_change = 1
        if reverse:
            minutess_to_change = -1
        d = d + datetime.timedelta(minutes=minutess_to_change)
        self.alarm_config[HOUR] = str(d.hour)
        self.alarm_config[MINUTE] = str(d.minute)
        self.set_alarm_time(d.hour, d.minute)
        self.changed_config = True

    def set_alarm_time(self, hour, minute):
        # Sets the time for when the alarm will go off

        self.turn_off_alarm()
        alarm_hour = int(hour)
        alarm_min = int(minute)
        d = datetime.datetime.now()
        alarm_today = datetime.datetime.combine(d.date(), d.time().replace(alarm_hour, alarm_min, 0, 0))
        alarm_tomorrow = datetime.datetime.combine(d.date() + datetime.timedelta(days=1),
                                                   d.time().replace(alarm_hour, alarm_min, 0, 0))

        if datetime.datetime.now() >= alarm_today:
            self.alarm_time = alarm_tomorrow
        else:
            self.alarm_time = alarm_today

    def update(self):
        self.changed_config = False
        current_time = datetime.datetime.now()
        if current_time > self.alarm_time:
            if self._is_alarm_enabled:
                self.turn_on_alarm()
            else:
                # resets alarm for the next day
                self.set_alarm_time(self.alarm_config[HOUR], self.alarm_config[MINUTE])

        if not pygame.mixer.music.get_busy() and self._is_alarm_on:
            pygame.mixer.music.play(-1)

        if not self._is_alarm_on and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def turn_on_alarm(self):
        self._is_alarm_on = True
