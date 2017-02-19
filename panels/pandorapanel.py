from .ipanel import IPanel
from enumbutton import EnumButton
from .lcddisplaydesigner import LCDDisplayDesigner

PANDORA_CONFIG = "Pandora"
SHOW_CURRENT_SONG = 0
SHOW_STATIONS = 1
NO_SONG_PLAYING = "No Song Playing"
AD_TEXT = "Ad"


class PandoraPanel(IPanel):

    def __init__(self, config, pydoracontroller):
        self.config = config[PANDORA_CONFIG]
        self.controller = pydoracontroller
        self.current_panel = SHOW_CURRENT_SONG
        self.next_station_index = None

    def process_keys(self, keys_pressed, keys_down):
        """process the keys, enter held down to get current station, but left and right to scroll
        select held down + right to stop/start
        select held down + left to skip
        """

        if EnumButton.ENTER in keys_down:
            # shows the stations to be selected
            if self.next_station_index is None:
                self.next_station_index = self.controller.get_current_station_index()
            self.current_panel = SHOW_STATIONS

            if EnumButton.LEFT in keys_pressed:
                self.next_station_index -= 1
            elif EnumButton.RIGHT in keys_pressed:
                self.next_station_index += 1

            if self.next_station_index < 0:
                self.next_station_index = len(self.controller.get_stations())-1
            elif self.next_station_index >= len(self.controller.get_stations()):
                self.next_station_index = 0
            return True
        else:
            self.current_panel = SHOW_CURRENT_SONG

            # changes the station if needed
            if self.next_station_index is not None:
                if self.next_station_index != self.controller.get_current_station_index():
                    self.controller.set_current_station_index(self.next_station_index)
                    self.controller.change_station()
                self.next_station_index = None

            if EnumButton.SELECT in keys_down:
                # stop / start and skip commands
                if EnumButton.RIGHT in keys_pressed:
                    if self.controller.is_active():
                        self.controller.stop()
                    else:
                        self.controller.play()
                elif EnumButton.LEFT in keys_pressed:
                    if self.controller.is_active():
                        self.controller.skip()
                return True
            else:
                return False

    def get_display(self):
        lcd = LCDDisplayDesigner()
        if self.current_panel == SHOW_CURRENT_SONG:
            song = self.controller.get_current_song()
            if song is None:
                lcd.center_top = NO_SONG_PLAYING
            elif song.is_ad:
                lcd.center_top = AD_TEXT
            else:
                lcd.center_top = song.song_name
                lcd.center_bottom = song.artist_name
        elif self.current_panel == SHOW_STATIONS:

            if self.next_station_index == self.controller.get_current_station_index:
                lcd.center_top = self.controller.get_current_station().name
            else:
                lcd.center_top = self.controller.get_stations()[self.next_station_index].name
        return lcd
