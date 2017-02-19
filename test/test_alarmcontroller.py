from unittest import TestCase
import datetime
import time
from controllers.alarmcontroller import AlarmController


class TestAlarmController(TestCase):
    def setUp(self):
        alarmtime = datetime.datetime.now() + datetime.timedelta(minutes=1)
        h = str(alarmtime.hour)
        m = str(alarmtime.minute)

        config = {'General': {
            "time-format": "%I:%M",
            "date-format": "%m %d"
        }, "Alarm": {
            "hour": h,
            "minute": m,
            "snooze": str(1),
            'alarm-enabled': str(True)
        }}

        config2 = {'General': {
            "time-format": "%I:%M",
            "date-format": "%m %d"
        }, "Alarm": {
            "hour": 0,
            "minute": 0,
            "snooze": str(1),
            'alarm-enabled': str(True)
        }}

        self.controller = AlarmController(config)
        self.controller_midnight_alarm = AlarmController(config2)

    def test_snooze(self):
        print("Starting Snooze Test")
        self.controller.alarm_time = datetime.datetime.now()

        time1 = self.controller.alarm_time
        self.controller.snooze()
        time2 = self.controller.alarm_time
        self.assertTrue(time2 > time1)
        self.assertFalse(self.controller.has_changed_config())
        print("Ending Snooze Test")

    def test_add_hour_to_alarm(self):
        print("Starting Add Hour To Alarm Test")
        time1 = self.controller.alarm_time
        self.controller.add_hour_to_alarm_config()
        time2 = self.controller.alarm_time

        time3 = self.controller.alarm_time
        self.controller.add_hour_to_alarm_config(True)
        time4 = self.controller.alarm_time

        self.assertEqual((time2 - time1).seconds, 60 * 60)
        self.assertEqual((time3 - time4).seconds, 60 * 60)
        self.assertTrue(self.controller.has_changed_config())
        print("Finish Add Hour To Alarm Test")

    def test_alarm_hour_roll_over(self):
        print("Starting Add Hour Rollover To Alarm Test")
        self.controller_midnight_alarm.set_alarm_time(0,0)
        t = self.controller_midnight_alarm.alarm_time
        self.controller_midnight_alarm.add_hour_to_alarm_config()
        t2 = self.controller_midnight_alarm.alarm_time
        self.controller_midnight_alarm.add_hour_to_alarm_config(True)
        t4 = self.controller_midnight_alarm.alarm_time

        self.assertEqual((t2-t).seconds, 60*60)
        self.assertEqual((t2-t4).seconds, 60*60)

        self.assertTrue(self.controller_midnight_alarm.has_changed_config())
        print("Finishing Add Hour Rollover To Alarm Test")


    def test_alarm_minute_roll_over(self):
        print("Starting Add Minute Rollover To Alarm Test")
        self.controller_midnight_alarm.set_alarm_time(0,0)
        t = self.controller_midnight_alarm.alarm_time
        self.controller_midnight_alarm.add_minute_to_alarm_config()
        t2 = self.controller_midnight_alarm.alarm_time
        self.controller_midnight_alarm.add_minute_to_alarm_config(True)
        t4 = self.controller_midnight_alarm.alarm_time

        self.assertEqual((t2-t).seconds, 60)
        self.assertEqual((t2-t4).seconds, 60)

        self.assertTrue(self.controller_midnight_alarm.has_changed_config())
        print("Finishing Add Minute Rollover To Alarm Test")

    def test_add_minute_to_alarm(self):
        print("Starting Add Minute To Alarm Test")
        time1 = self.controller.alarm_time
        self.controller.add_minute_to_alarm_config()
        time2 = self.controller.alarm_time

        time3 = self.controller.alarm_time
        self.controller.add_minute_to_alarm_config(True)
        time4 = self.controller.alarm_time

        self.assertEqual((time2 - time1).seconds, 60)
        self.assertEqual((time3 - time4).seconds, 60)
        self.assertTrue(self.controller.has_changed_config())
        print("Finishing Add Minute To Alarm Test")

    def test_set_alarm_time(self):
        print("Starting set alarm test")
        time1 = self.controller.alarm_time
        d = time1 + datetime.timedelta(minutes=1)
        self.controller.set_alarm_time(d.hour, d.minute)
        time2 = self.controller.alarm_time
        self.assertTrue((time2-time1).seconds, 60)
        print("Finishing set alarm test")

    def test_alarm(self):
        print("Starting Alarm test")
        self.controller.update()
        time.sleep(90)
        self.controller.update()
        self.assertTrue(self.controller._is_alarm_on)
        time.sleep(2)
        self.controller.snooze()
        self.assertFalse(self.controller._is_alarm_on)
        self.assertFalse(self.controller.has_changed_config())
        print("Finishing Alarm test")