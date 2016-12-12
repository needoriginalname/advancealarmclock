from tkwindow import TKWIndow
from configparser import ConfigParser
from tkwindow import TKWIndow
import os.path as path

FILE = "alarmclock.cfg"

def setup_config_parser():
    config = ConfigParser()
    config.read(FILE)
    return config

def start():
    config = setup_config_parser()
    t = TKWIndow(config)
    t.start(config)

if __name__ == "__main__":
    start()


