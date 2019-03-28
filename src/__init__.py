import json
import os


config_file = "config.json"

if not os.path.isfile(config_file):
    # For testing purposes
    config_file = "../config.json"

with open(config_file, "r") as cfg:
    config = json.load(cfg)

# There must be a better way to store commands...
cmds = {}


def add_handler(cmd, handler):
    cmds[cmd] = handler


# Must be imported here
from .commands import *


def cmd_lookup(cmd):
    if cmd in cmds:
        return cmds[cmd]
    return None

