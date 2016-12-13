import sys
from pandora import clientbuilder

from controllers.pydoraplayer import PydoraPlayer
import os
import pydora.player


class PydoraController:
    def __init__(self, config):
        self.player = PydoraPlayer(None, os.devnull)
        self.client = None
        self.stations = None

    def get_client(self):
        cfg_file = os.environ.get("PYDORA_CFG", "")
        builder = clientbuilder.PydoraConfigFileBuilder(cfg_file)
        if builder.file_exists:
            return builder.build()

        builder = clientbuilder.PianobarConfigFileBuilder()
        if builder.file_exists:
            return builder.build()

        if not self.client:
            print("No valid config found")
            sys.exit(1)

    def run(self):
        self.client = self.get_client()
        self.stations = self.client.get_station_list()

    def stop(self):
        self.player.end_station()

    def get_stations(self):
        return self.stations

    def play(self, i):
        self.player.play_station(self.get_stations()[i])

    def pause(self):
        self.player.pause()

    def skip(self):
        if not self.player.song.is_ad:
            self.player.stop()
