from unittest import TestCase
from controllers.weathercontroller import WeatherController
from panels.weatherpanel import WeatherPanel
from enumbutton import EnumButton


class TestWeatherPanel(TestCase):
    def setUp(self):
        config = {'Weather': {
            'unit': "fahrenheit",
            'api-key': 'fe2a0bb52f153e98341db686394423e4',
            'location-code': '43223',
            'update-time': '300000'
        }, 'General': {
            "time-format": "%I:%M",
            "date-format": "%m %d"
        }}

        self.controller = WeatherController(config)
        self.panel = WeatherPanel(config, self.controller)

    def test_process_keys(self):
        self.assertTrue(self.panel._panel_index == 0)
        self.assertFalse(self.panel.process_keys([], []))
        self.assertTrue(self.panel.process_keys([],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 1)
        self.assertTrue(self.panel.process_keys([EnumButton.RIGHT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 2)
        self.assertTrue(self.panel.process_keys([EnumButton.RIGHT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 3)
        self.assertTrue(self.panel.process_keys([EnumButton.RIGHT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 1)
        self.assertTrue(self.panel.process_keys([EnumButton.LEFT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 3)
        self.assertTrue(self.panel.process_keys([EnumButton.LEFT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 2)
        self.assertTrue(self.panel.process_keys([EnumButton.LEFT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 1)
        self.assertTrue(self.panel.process_keys([EnumButton.LEFT],[EnumButton.ENTER]))
        self.assertEqual(self.panel._panel_index, 3)
        self.assertFalse(self.panel.process_keys([EnumButton.LEFT],[]))
        self.assertEqual(self.panel._panel_index, 0)
        self.assertFalse(self.controller.has_changed_config())

    def test_get_display(self):
        self.panel._panel_index = 0
        print(self.panel.get_display())
        self.panel._panel_index = 1
        print(self.panel.get_display())
        self.panel._panel_index = 2
        print(self.panel.get_display())
        self.panel._panel_index = 3
        print(self.panel.get_display())
        self.assertFalse(self.controller.has_changed_config())
