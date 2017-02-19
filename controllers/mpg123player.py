import logging
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
        logging.debug(str(c))
        self._process = subprocess.Popen(c)

    def play(self, song):
        self.song = song
        if song.is_ad:
            logging.info("playing an ad")
        else:
            logging.info("play {} : {}".format(song.song_name, song.artist_name))

        self._send_cmd(song.audio_url)

    def update(self):
        try:
            if self._process:
                    if self._player_stopped():
                        logging.info("player not on, playing station")
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
                logging.info("playlist empty, getting a new one")
                self._playlist = station.get_playlist()
            try:
                song = None
                try:
                    logging.info("getting a new song from playlist")
                    item = next(self._playlist)
                    item.prepare_playback()
                    song = item
                except StopIteration:
                    # get playlist again, if fails player will stop
                    logging.warning("playlist iterator failed, attempting again")
                    self._playlist = station.get_playlist()
                    item = next(self._playlist)
                    item.prepare_playback()
                    song = item
                self.play(song)
            except StopIteration:
                logging.error("unable to get playlist after second attempt")
                self.stop()
        else:
            logging.error("no station found")

    def end_station(self):
        logging.info("stopping station, and clearing playlist")
        self.stop()
        self._playlist = None

    def stop(self):
        logging.info("stopping player")
        self.song = None
        if self._process:
            logging.info("ending mpg123 process")
            self._process.kill()

    def skip(self):
        if self.song is not None and not self.song.is_ad:
            self.stop()
            self.play_station()
        elif self.song is not None and self.song.is_ad:
            logging.warning("skip request received, ignoring due to ad")
        else:
            logging.warning("skip request received, nothing to skip")

    def _player_stopped(self):
        if self._process is None or self._process.poll() is not None:
            return True
        else:
            return False
