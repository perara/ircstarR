import json
import os

from src.misc.bunch import Bunch

config_file = "config.json"

if not os.path.isfile(config_file):
    # For testing purposes
    config_file = "../config.json"

with open(config_file, "r") as cfg:
    config = json.load(cfg)


