from unittest import TestCase
import os
import subprocess

import time

from controllers.pydoracontroller import PydoraController
from enumbutton import EnumButton
from panels.pandorapanel import PandoraPanel
from panels.pandorapanel import AD_TEXT
from panels.pandorapanel import NO_SONG_PLAYING

LAST_PANEL_INDEX = "last-station-index"
PYDORA_CONFIG_LOC = "Pandora"


class TestPandoraPanel(TestCase):
    def setUp(self):
        self.config = dict()
        pydora_config = dict()
        pydora_config[LAST_PANEL_INDEX] = str(1)
        self.config[PYDORA_CONFIG_LOC] = pydora_config

        self.controller = PydoraController(self.config)
        self.panel = PandoraPanel(self.config, self.controller)

    def test_no_song_playing(self):
        print("No song playing test")
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])
        self.assertFalse(self.controller.has_changed_config())

    def test_stopped_song_after_playing(self):
        print("song stopped after playing test")
        self.start_stop_playing_keys(self.panel)
        time.sleep(15)
        self.start_stop_playing_keys(self.panel)
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])
        self.assertFalse(self.controller.has_changed_config())

    def test_song_playing(self):
        print("song playing test")
        self.start_stop_playing_keys(self.panel)
        time.sleep(15)
        self.assertFalse(NO_SONG_PLAYING in self.panel.get_display()[0])
        self.assertFalse(self.controller.has_changed_config())

    def test_song_changing(self):
        # test can fail if audio file is very very long

        print("song changing test")
        self.start_stop_playing_keys(self.panel)
        song1 = self.panel.get_display()[0]
        for i in range(300):
            time.sleep(1)
            self.controller.update()
        song2 = self.panel.get_display()[0]
        self.assertNotEqual(song1, song2)
        self.assertFalse(self.controller.has_changed_config())

    def test_song_skip(self):
        print("song skip test")
        self.start_stop_playing_keys(self.panel)
        self.hold_if_ad(self.controller, self.panel)
        self.assertFalse(self.controller.has_changed_config())

        song1 = self.panel.get_display()[0]
        time.sleep(10)
        self.skip_keys(self.panel)
        song2 = self.panel.get_display()[0]
        self.assertNotEqual(song1, song2)

    def test_show_station_while_stopped(self):
        print("show station while stopped test")
        song_title = self.get_first_display_song(self.panel)
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])

        self.show_change_station_keys(self.panel)
        station_title = self.get_first_display_song(self.panel)
        self.assertNotEqual(song_title, station_title)

        self.all_keys_up(self.panel)
        # song_title2 = self.get_first_display_song(self.panel)
        self.assertFalse(self.controller.has_changed_config())
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])

    def test_show_station_while_playing(self):
        print("show station while playing test")
        self.start_stop_playing_keys(self.panel)
        song_title = self.get_first_display_song(self.panel)

        self.show_change_station_keys(self.panel)
        station_title = self.get_first_display_song(self.panel)
        self.assertNotEqual(song_title, station_title)

        self.all_keys_up(self.panel)
        song_title2 = self.get_first_display_song(self.panel)

        self.assertEqual(song_title, song_title2)
        self.assertFalse(self.controller.has_changed_config())

    def test_scroll_stations_while_stopped(self):
        print("scroll station while stopped test")
        song_title = self.get_first_display_song(self.panel)
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])
        self.show_change_station_keys(self.panel)
        station_name = self.get_first_display_song(self.panel)
        self.show_change_station_keys(self.panel, EnumButton.RIGHT)
        station_name2 = self.get_first_display_song(self.panel)

        self.assertNotEqual(station_name, station_name2)
        self.show_change_station_keys(self.panel, EnumButton.LEFT)
        station_name3 = self.get_first_display_song(self.panel)
        self.assertEqual(station_name, station_name3)

        self.all_keys_up(self.panel)
        song_title2 = self.get_first_display_song(self.panel)
        self.assertEqual(song_title, song_title2)
        self.assertFalse(self.controller.has_changed_config())

    def test_scroll_stations_while_playing(self):
        print("scroll station while playing test")
        self.start_stop_playing_keys(self.panel)

        song_title = self.get_first_display_song(self.panel)
        self.show_change_station_keys(self.panel)
        station_name = self.get_first_display_song(self.panel)
        self.show_change_station_keys(self.panel, EnumButton.RIGHT)
        station_name2 = self.get_first_display_song(self.panel)

        self.assertNotEqual(station_name, station_name2)
        self.show_change_station_keys(self.panel, EnumButton.LEFT)
        station_name3 = self.get_first_display_song(self.panel)
        self.assertEqual(station_name, station_name3)

        self.all_keys_up(self.panel)
        song_title2 = self.get_first_display_song(self.panel)
        self.assertEqual(song_title, song_title2)
        self.assertFalse(self.controller.has_changed_config())

    def test_change_station_while_playing(self):
        print("change station while playing test")

        self.start_stop_playing_keys(self.panel)
        song_title1 = self.get_first_display_song(self.panel)

        # change station
        self.show_change_station_keys(self.panel)
        station1 = self.get_first_display_song(self.panel)
        self.show_change_station_keys(self.panel, EnumButton.RIGHT)
        station2 = self.get_first_display_song(self.panel)
        self.all_keys_up(self.panel)

        # check new station name
        self.show_change_station_keys(self.panel)
        station3 = self.get_first_display_song(self.panel)
        self.assertEqual(station2, station3)
        self.assertNotEqual(station1, station3)
        self.all_keys_up(self.panel)

        # check new song name
        song_title2 = self.get_first_display_song(self.panel)
        self.assertNotEqual(song_title1, song_title2)
        self.assertTrue(self.controller.has_changed_config())

    def test_change_station_while_stopped(self):
        print("change station while stopped test")
        song_title1 = self.get_first_display_song(self.panel)

        # change station
        self.show_change_station_keys(self.panel)
        station1 = self.get_first_display_song(self.panel)
        self.show_change_station_keys(self.panel, EnumButton.RIGHT)
        station2 = self.get_first_display_song(self.panel)
        self.all_keys_up(self.panel)

        # check new station name
        self.show_change_station_keys(self.panel)
        station3 = self.get_first_display_song(self.panel)
        self.assertEqual(station2, station3)
        self.assertNotEqual(station1, station3)
        self.all_keys_up(self.panel)

        # check new song name
        song_title2 = self.get_first_display_song(self.panel)
        self.assertEqual(song_title1, song_title2)
        self.assertTrue(NO_SONG_PLAYING in self.panel.get_display()[0])
        self.assertTrue(self.controller.has_changed_config())

    @staticmethod
    def show_change_station_keys(panel, button=None):
        pressed = []
        if button is None:
            pressed = []
        else:
            pressed = [button]
        down = [EnumButton.ENTER]
        panel.process_keys(keys_pressed=pressed, keys_down=down)

    @staticmethod
    def get_first_display_song(panel):
        print(panel.get_display()[0])
        return panel.get_display()[0]

    @staticmethod
    def start_stop_playing_keys(panel):
        pressed = [EnumButton.RIGHT]
        down = [EnumButton.SELECT]
        panel.process_keys(keys_pressed=pressed, keys_down=down)
        return panel

    @staticmethod
    def all_keys_up(panel):
        pressed = []
        down = []
        panel.process_keys(keys_pressed=pressed, keys_down=down)
        return panel

    @staticmethod
    def skip_keys(panel):
        pressed = [EnumButton.LEFT]
        down = [EnumButton.SELECT]
        panel.process_keys(keys_pressed=pressed, keys_down=down)
        return panel

    def tearDown(self):
        print("resetting test")
        print("")
        time.sleep(30)
        self.controller.stop()


    @staticmethod
    def hold_if_ad(controller, panel):
        print("Ad found, holding test till done")
        while panel.get_display()[0] == AD_TEXT:
            time.sleep(1)
            controller.update()
