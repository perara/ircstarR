from dataclasses import dataclass, field
from typing import Dict, Tuple, List


@dataclass
class Message:
    """ Message dataclass to be passed to through out the program """
    username: str
    userhost: str
    server_cmd: str
    channel: str
    msg: str
    cmd_args: List = field(default_factory=lambda: [])  # Not really needed as args will always be supplied..
