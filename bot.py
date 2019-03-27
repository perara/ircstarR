#!/usr/bin/python3
import socket
import time
import logging
import logging.config
import re

from src import config
from src.abstraction.models import Message

# Based on https://github.com/Orderchaos/LinuxAcademy-IRC-Bot/blob/master/bot.py

logging.config.dictConfig(config["logging"])
logger = logging.getLogger("test")

logger.info("Running")

cmds = {}  # Holds all commands functions


def add_handler(cmd, handler):
    cmds[cmd] = handler


def lookup(cmd):
    if cmd in cmds:
        return cmds[cmd]
    return None


class IRC:

    def __init__(self, config):
        self.server = config["server"]
        self.channel = config["channel"]
        self.bot_nick = config["bot_nick"]
        self.bot_admin = config["bot_admin"]
        self.exitcode = "bye " + self.bot_nick

        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.command_prefix = "."
        self.message_pattern = \
            re.compile(r"!~(?P<username>.+)\@(?P<userhost>.+) (?P<server_cmd>[A-Z]+) (?P<channel>(#?)\w+) :(?P<msg>.+)\r\n")

        self.isConnected = False

    def connect(self):
        """ Connect to IRC server """
        self.ircsock.connect((self.server, 6667))  # Here we connect to the server using the port 6667
        self.ircsock.send(
            bytes(f"USER {self.bot_nick} {self.bot_nick} {self.bot_nick} {self.bot_nick} \n", "UTF-8"))
        self.ircsock.send(bytes(f"NICK  {self.bot_nick} \n", "UTF-8"))  # assign the nick to the bot

        self.isConnected = True

    def pong(self):
        """" Respond to server Pings """
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
        logger.debug("Sent PONG to server")

    def join_channel(self):  # join channel(s).

        self.ircsock.send(bytes(f"JOIN {self.channel} \n", "UTF-8"))

        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            print(ircmsg)

        logger.info(f"Joined channel {self.channel} as {self.bot_nick}")

    def sendmsg(self, message, target):
        """ Send PRIVMSG to target ex channel or a user chat """
        # With this we are sending a ‘PRIVMSG’ to the channel. The ":” lets the server separate the target and the message.
        if not target:
            target = self.channel

        self.ircsock.send(bytes(f"PRIVMSG {target} : {message} \n", "UTF-8"))
        logger.info(f"Sent message '{message}' to {target}")

    def run_bot(self):
        """ Run the IRC bot """
        self.connect()
        if not self.isConnected:
            logger.error("Could not connect")
            exit(1)

        self.join_channel()

        while 1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")

            if ircmsg.startswith("PING"):
                logger.debug("Received PING from server")
                self.pong()
                continue

            parsed_msg = re.search(self.message_pattern, ircmsg)

            if not parsed_msg:
                logger.warning("Unable to parse message: %s", ircmsg)
                continue

            msg_obj = Message(**parsed_msg.groupdict())

            if not msg_obj.msg.startswith(self.command_prefix):
                # Not a command, lets move on..
                logger.debug(f"{msg_obj.msg} Not a command..")
                continue

            # We have a 'command' - Lets try to Handle the command
            cmd, *args = msg_obj.msg.split()
            logger.debug(f"cmd: {cmd} args: {args}")
            cmd = cmd[1:]  # Remove command prefix

            command_handler = lookup(cmd)
            if command_handler:
                logger.debug(f"Command '{cmd}' has handler func '{command_handler.__name__}'")
                msg_obj.cmd_args = args
                # Execute the function to the corresponding command
                # Could also execute the function and send the return value as the response here
                # instead of in the command function.
                command_handler(msg=msg_obj, bot=self)
            else:
                # Received an unknown command
                self.sendmsg(f"Unknown command. No command handlers for command '{self.command_prefix + cmd}'",
                             target=msg_obj.channel)


def test_cmd(msg: Message, bot: IRC):
    time.sleep(5)
    bot.sendmsg("test_cmd sleept for 5 sec", target=msg.channel)


add_handler("testcmd", test_cmd)


def echo(msg: Message, bot: IRC):
    bot.sendmsg(message=msg.msg, target=msg.channel)


add_handler("echo", echo)


bot = IRC(config)
bot.run_bot()
