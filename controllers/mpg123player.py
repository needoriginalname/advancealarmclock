import subprocess


class MPG123Player():
    def __init__(self):
        self.station = None
        self.song = None
        self._playlist = None
        self._process = None

        wd = "C:\\Users\\Owner\\Downloads\\mpg123-1.23.4-x86-64\\mpg123-1.23.4-x86-64\\"
        import os
        os.chdir(wd)
        self.command_string = wd + "mpg123.exe"

    def __del__(self):
        if self._process:
            self._process.kill()

    def _send_cmd(self, command):
        if self._process:
            self._process.kill()

        c = [self.command_string, "-q", "--ignore-mime", command]
        print(c)
        self._process = subprocess.Popen(c)

    def play(self, song):
        self.song = song
        self._send_cmd(song.audio_url)

    def update(self):
        try:
            if self._process:
                    if self._player_stopped():
                        self.play_station()
        finally:
            pass

    def pause(self):
        pass

    def play_station(self, station=None):
        if station is None:
            station = self.station
        else:
            self.station = station

        if station:
            if self._playlist is None:
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
        if self._process:
            self._process.kill()

    def skip(self):
        if self.song is not None and not self.song.is_ad:
            self.stop()
            self.play_station()

    def _player_stopped(self):
        if self._process is None or self._process.poll() is not None:
            return True
        else:
            return False
