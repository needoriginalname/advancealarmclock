from unittest import TestCase
from controllers.pydoracontroller import PydoraController
import time
class TestPydoraController(TestCase):

    def setUp(self):
        self.controller = PydoraController(None)

    def test_playing(self):
        print("testing play")
        self.controller.play(1)
        time.sleep(5)
        self.controller.stop()

    def test_get_station_list(self):
        print("testing station list")
        for station in self.controller.get_stations():
            print(station)

    def test_skip(self):
        print("test skip")
        self.controller.play(1)
        time.sleep(2)
        self.controller.skip()
        time.sleep(2)

    def test_pause(self):
        print("test skip")
        self.controller.play(1)
        time.sleep(2)
        self.controller.pause()
        time.sleep(2)
        self.controller.pause()
            
    def tearDown(self):
        self.controller.stop()
        time.sleep(5)
        
