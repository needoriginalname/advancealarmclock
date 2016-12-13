from pydora.mpg123 import Player
from pydora.utils import iterate_forever
import select


class PydoraPlayer(Player):
    def __init__(self, callbacks, control_channel):
        super.__init__(callbacks, control_channel)
        self.station = None
        self.song = None

    def play(self, song):
        self.song = song
        self._callbacks.play(song)
        self._send_cmd("load {}".format(song.audio_url))

    def update(self):

        try:
            self._ensure_started()
            if self._process:
                readers, _, _ = select.select(
                    [self._control_channel, self._process.stdout], [], [], 1)

                for handle in readers:
                    value = handle.readline().strip()
                    if self._player_stopped(value):
                        self.play_station()
        finally:
            pass

    def play_station(self, station=None):
        if station is None:
            station = self.station
        else:
            self.station = station

        if station:
            song = iterate_forever(station.get_playlist)
            try:
                self.play(song)
            except StopIteration:
                self.stop()

    def end_station(self):
        self.stop()

    def stop(self):
        self.song = None
        super().stop()



