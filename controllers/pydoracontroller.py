import sys
from pandora import clientbuilder

from controllers.pydoraplayer import PydoraPlayer
import os
import sys
import pydora.player
from pydora.player import PlayerCallbacks
INDEX = "last-station-index"

class PydoraController():
    def __init__(self, config):
        callbacks = PlayerCallbacks()
        self.player = PydoraPlayer(callbacks, sys.stdin)
        self.client = self.get_client()
        self.stations = self.client.get_station_list()
        self.config = config["pydora"]
        self._is_active = False
        self._station_index = int()

    def is_active(self):
        return self._is_active

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
        self._is_active = False

    def get_stations(self):
        return self.stations

    def get_current_station(self):
        return self.stations[self.get_current_station_index()]

    def get_current_song(self):
        return self.player.song

    def get_current_station_index(self):
        return self.config[INDEX]

    def set_current_station_index(self, n):
        self.config[INDEX] = n

    def play(self):
        self.player.play_station(station=self.get_current_station())
        self._is_active = True

    def pause(self):
        self.player.pause()

    def change_station(self):
        self.stop()
        self.play()

    def skip(self):
        self.player.skip()

    def update(self):
        if self._is_active:
            self.player.update()


if __name__ == "__name__":
    p = PydoraController(None)
    p.play(1)
