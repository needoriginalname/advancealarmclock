from panels.ipanel import IPanel
import math
import datetime
from enumbutton import EnumButton
from panels.lcddisplaydesigner import LCDDisplayDesigner

GENERAL = "General"
EXTENDED_TIME_FORMAT = "extended-time-format"
EXTENDED_DATE_FORMAT = "extended-date-format"

ALARM_FORMAT = "alarm-format"
HOUR_BLINK_ALARM_FORMAT = "hour-blink-alarm-format"
MINUTE_BLINK_ALARM_FORMAT = "minute-blink-alarm-format"
ALARM_TIME_STRING = "Alarm Time"

class TimePanel(IPanel):
    def get_display(self):
        result = ["", ""]
        lcd = LCDDisplayDesigner()
        if self._panel_index == 0:
            lcd.center_top = datetime.datetime.now().strftime(self.config[EXTENDED_TIME_FORMAT])
            lcd.center_bottom = datetime.datetime.now().strftime(self.config[EXTENDED_DATE_FORMAT])
        else:
            lcd.center_top = ALARM_TIME_STRING
            if (datetime.datetime.now() - self._blink_change_time) > datetime.timedelta(milliseconds=500):
                self._blink_change_time = datetime.datetime.now()
                self._blink = not self._blink

            if self._blink:
                if self._panel_index == 1:
                    lcd.center_top = self.alarm_controller.alarm_time.strftime(self.config[HOUR_BLINK_ALARM_FORMAT])
                else:
                    lcd.center_top = self.alarm_controller.alarm_time.strftime(self.config[MINUTE_BLINK_ALARM_FORMAT])
            else:
                lcd.center_bottom = self.alarm_controller.alarm_time.strftime(self.config[ALARM_FORMAT])
        return lcd

    def process_keys(self, keys_pressed, keys_down):
        if EnumButton.ENTER in keys_down:
            self.alarm_controller.reset_alarm_from_configs()
            if self._panel_index == 0:
                self._panel_index = 1

            # add or subtract the minute or hour
            if EnumButton.RIGHT in keys_pressed or EnumButton.LEFT in keys_pressed:
                b = False
                if EnumButton.LEFT in keys_pressed:
                    b = True
                if self._panel_index == 1:
                    self.alarm_controller.add_hour_to_alarm_config(b)
                else:
                    self.alarm_controller.add_minute_to_alarm_config(b)

            # navigate between hour and minute alarm setting
            if EnumButton.SELECT in keys_pressed:
                if self._panel_index == 1:
                    self._panel_index = 2
                else:
                    self._panel_index = 1
            return True
        else:
            self._panel_index = 0
            if EnumButton.SELECT in keys_pressed:
                self.alarm_controller.snooze()
                return True
            return False

    def __init__(self, config, alarmcontroller):
        self.alarm_controller = alarmcontroller
        self.config = config[GENERAL]
        self._panel_index = 0
        self._blink = False
        self._blink_change_time = datetime.datetime.now()

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
