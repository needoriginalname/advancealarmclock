from unittest import TestCase
import datetime
from controllers.alarmcontroller import AlarmController
from enumbutton import EnumButton
from panels.timepanel import TimePanel


class TestTimePanel(TestCase):
    def setUp(self):
        alarmtime = datetime.datetime.now() + datetime.timedelta(minutes=1)
        h = str(alarmtime.hour)
        m = str(alarmtime.minute)
        config = {'Weather': {
            'unit': "fahrenheit",
            'api-key': 'fe2a0bb52f153e98341db686394423e4',
            'location-code': '43223',
            'update-time': '300000'
        }, 'General': {
            "time-format": "%I:%M %p",
            "alarm-format": "%I:%M %p",
            "hour-blink-alarm-format": "  :%M %p",
            "minute-blink-alarm-format": "%I:   %p",
            "date-format": "%m %d",
            "extended-date-format": "%a %b %d %Y",
            "extended-time-format": "%I:%M:%S %p"

        }, "Alarm": {
            "hour": h,
            "minute": m,
            "snooze": str(1),
            'alarm-enabled': str(True)
        }}

        alarm_controller = AlarmController(config)
        self.panel = TimePanel(alarm_controller, config)

    def test_display(self):
        self.panel._panel_index = 0
        print(self.panel.get_display())
        self.panel._panel_index = 1
        self.panel._blink = False
        print(self.panel.get_display())
        self.panel._blink = True
        print(self.panel.get_display())
        self.panel._panel_index = 2
        self.panel._blink = False
        print(self.panel.get_display())
        self.panel._blink = True
        print(self.panel.get_display())

    def test_change_hour(self):
        self.panel._panel_index = 0
        self.panel.process_keys([], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 1)

        print(self.panel.get_display())
        self.panel.process_keys([EnumButton.RIGHT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 1)
        print(self.panel.get_display())
        self.panel.process_keys([EnumButton.LEFT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 1)
        print(self.panel.get_display())

    def test_change_minute(self):
        self.panel._panel_index = 0
        self.panel.process_keys([], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 1)

        self.panel.process_keys([EnumButton.SELECT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 2)
        print(self.panel.get_display())
        self.panel.process_keys([EnumButton.RIGHT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 2)
        print(self.panel.get_display())
        self.panel.process_keys([EnumButton.LEFT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 2)
        print(self.panel.get_display())
        self.panel.process_keys([EnumButton.SELECT], [EnumButton.ENTER])
        self.assertEqual(self.panel._panel_index, 1)

        self.panel.process_keys([], [])
        self.assertEqual(self.panel._panel_index, 0)
