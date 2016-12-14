from pydora.mpg123 import Player
from pydora.utils import iterate_forever
import select


class PydoraPlayer(Player):
    def __init__(self, callbacks, control_channel):
        self.station = None
        self.song = None
        self._playlist = None
        self._control_channel = control_channel
        self._callbacks = callbacks
        self._process = None
        self._ensure_started()

    def play(self, song):
        self.song = song
        self._callbacks.play(song)
        self._send_cmd("load {}".format(song.audio_url))
        if not song.is_ad:
            print(song.song_name)

    def update(self):

        try:
            self._ensure_started()
            if self._process:
                readers, _, _ = select.select(
                    [self._process.stdout], [], [], 1)

                for handle in readers:
                    value = handle.readline().strip()
                    print(value)
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

            if (self._playlist is None):
                self._playlist = station.get_playlist()
                
            try:
                song = None
                try:
                    item = next(self._playlist)
                    item.prepare_playback()
                    song = item
                except StopIteration:
                    # get playlist again, if fails player will stop
                    self._playlist = station.get_playlist()
                    item = next(self._playlist)
                    item.prepare_playback()
                    song = item
                self.play(song)
            except StopIteration:
                self.stop()

    def end_station(self):
        self.stop()

    def stop(self):
        self.song = None
        super().stop()



