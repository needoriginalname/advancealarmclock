import simpleaudio
import datetime
import os


class AlarmController:
    def __init__(self, config):
        self.alarm_config = config['Alarm']
        self.config = config['General']

        # setup the alarm sound
        sound_filepath = os.path.join(os.path.dirname(__file__), 'alarm.wav')
        self.sound_file = simpleaudio.WaveObject.from_wave_file(sound_filepath)
        self._is_alarm_enabled = self.alarm_config['alarm-enabled']
        self._is_alarm_on = False
        self.audio_playing = None

        # sets the alarm time
        self.alarm_time = None
        self.set_alarm_time(int(self.alarm_config['hour']), int(self.alarm_config['minute']))
        self.snooze_time = int(self.alarm_config['snooze'])



    def turn_off_alarm(self):
        if self._is_alarm_on:
            self._is_alarm_on = False

    def snooze(self):
        time_now = datetime.datetime.now().replace(second=0, microsecond=0)
        time_snooze = time_now + datetime.timedelta(minutes=self.snooze_time)

        self.set_alarm_time(time_snooze.hour, time_snooze.minute)

    def add_hour_to_alarm_config(self, reverse = False):
        alarm_hour = int(self.alarm_config['hour'])
        alarm_min = int(self.alarm_config['minute'])
        d = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_min,second=0,microsecond=0)
        hoursToChange = 1
        if reverse:
            hoursToChange = -1
        d = d + datetime.timedelta(hours=hoursToChange)
        self.alarm_config['hour'] = str(d.hour)
        self.alarm_config['minute'] = str(d.minute)
        self.set_alarm_time(d.hour, d.minute)

    def add_minute_to_alarm_config(self, reverse=False):
        alarm_hour = int(self.alarm_config['hour'])
        alarm_min = int(self.alarm_config['minute'])
        d = datetime.datetime.now().replace(hour=alarm_hour, minute=alarm_min, second=0, microsecond=0)
        minutessToChange = 1
        if reverse:
            minutessToChange = -1
        d = d + datetime.timedelta(minutes=minutessToChange)
        self.alarm_config['hour'] = str(d.hour)
        self.alarm_config['minute'] = str(d.minute)
        self.set_alarm_time(d.hour, d.minute)

    def set_alarm_time(self, hour, minute):
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
        current_time = datetime.datetime.now()
        if current_time > self.alarm_time:
            if self._is_alarm_enabled:
                self._is_alarm_on = True
            else:
                # resets alarm for the next day
                self.set_alarm_time(self.alarm_config['hour'], self.alarm_config['min'])

        if self._is_alarm_on and (self.audio_playing is None or (not self.audio_playing.is_playing())):
            self.audio_playing = self.sound_file.play()
        else:
            if self.audio_playing is not None and self.audio_playing.is_playing():
                self.audio_playing.stop()

    @staticmethod
    def _wrap(n, min_value, max_value):
        if n > max_value:
            n = (n - max_value) + min_value

        if n < min_value:
            n = max_value - (min_value - n)

        return n
