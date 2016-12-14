import sys
from pandora import clientbuilder

from controllers.pydoraplayer import PydoraPlayer
import os
import sys
import pydora.player
from pydora.player import PlayerCallbacks


class PydoraController():
    def __init__(self, config):
        callbacks = PlayerCallbacks()
        self.player = PydoraPlayer(callbacks, sys.stdin)
        self.client = self.get_client()
        self.stations = self.client.get_station_list()

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

    def stop(self):
        self.player.end_station()

    def get_stations(self):
        return self.stations

    def play(self, i):
        self.player.play_station(station=self.get_stations()[i])

    def pause(self):
        self.player.pause()

    def skip(self):
        if song is not None and not self.player.song.is_ad:
            self.player.stop()
            self.player.play_station()

    def update(self):
        self.player.update()


if __name__ == "__name__":
    p = PydoraController(None)
    p.play(1)
