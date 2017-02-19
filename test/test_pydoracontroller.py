from unittest import TestCase

import subprocess

from controllers.pydoracontroller import PydoraController
from subprocess import Popen
import time


class TestPydoraController(TestCase):

    def setUp(self):
        config = dict()
        pydora_config = dict()
        pydora_config["last-station-index"] = str(2)
        config["Pandora"] = pydora_config

        self.controller = PydoraController(config)

    def test_playing(self):
        print("testing play")
        self.controller.play()
        time.sleep(30)
        self.assertFalse(self.controller.has_changed_config())
        self.controller.stop()

    def test_get_station_list(self):
        print("testing station list")
        for station in self.controller.get_stations():
            print(station)
        self.assertIsNotNone(self.controller.get_stations())
        self.assertFalse(self.controller.has_changed_config())

    def test_skip(self):
        print("test skip")
        self.controller.play()

        while self.controller.get_current_song().is_ad:
            # test does not work with an ad, keep playing till no longer ad.
            self.controller.update()

        time.sleep(5)
        song = self.controller.get_current_song()
        self.controller.skip()
        song2 = self.controller.get_current_song()
        time.sleep(5)
        self.assertNotEqual(song, song2)
        self.assertFalse(self.controller.has_changed_config())

    def test_long_play(self):
        print("test long play")
        self.controller.play()
        n_loops = 600
        while n_loops > 0:
            time.sleep(1)
            self.controller.update()
            print(n_loops)
            n_loops -= 1
        print("ending long play test")
        self.assertFalse(self.controller.has_changed_config())

    def test_failed_ad_skip(self):
        print("Starting failed ad skip")
        self.controller.play()
        while True:
            self.controller.update()
            song = self.controller.get_current_song()
            if song.is_ad:
                break

        print("Ad found")
        song = self.controller.get_current_song()
        self.controller.skip()
        print("Ad skip attempted")
        song2 = self.controller.get_current_song()
        self.assertEqual(song, song2)
        self.assertFalse(self.controller.has_changed_config())

    def test_start_stop_start_again(self):
        print("starting start stop start test")
        print("wait for it to start")
        for i in range(30):
            time.sleep(1)
            self.controller.update()

        self.controller.play()
        print("inital start")
        for i in range(30):
            time.sleep(1)
            self.controller.update()

        self.controller.stop()
        print("stop")
        for i in range(30):
            time.sleep(1)
            self.controller.update()

        self.controller.play()
        print("play again")
        for i in range(30):
            time.sleep(1)
            self.controller.update()
        print("ending")
        self.assertFalse(self.controller.has_changed_config())

    def tearDown(self):
        "30 pause between any tests to prevent getting a potential hit from Pandora"

        self.controller.stop()
        time.sleep(30)
