#!/usr/bin/python3
import time
import logging
import re

from src.irc import IRC
from src import commands
from src.abstraction.models import Message


logger = logging.getLogger("ircstarr.bot")


class Bot(IRC):
    def __init__(self, config):
        super().__init__(**config["irc"])
        self.config = config
        self.commands = commands.load()

    def run_forever(self):
        """ Run the IRC bot """
        # Connect to server
        self._connect()
        if not self.isConnected:
            logger.error("Could not connect")
            exit(1)

        time.sleep(1)  # Sleep for good reasons

        # Join channel
        self._join_channel()

        while 1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            if ircmsg: logger.debug(repr(ircmsg))

            if ircmsg.startswith("PING"):
                logger.debug("Received PING from server")
                self._pong()
                continue

            parsed_msg = re.search(self.message_pattern, ircmsg)

            if not parsed_msg:
                logger.warning("Unable to parse message: %s", repr(ircmsg))
                continue

            msg_obj = Message(**parsed_msg.groupdict())
            logger.debug(repr(msg_obj))

            if not msg_obj.msg.startswith(self.command_prefix):
                # Not a command, lets move on..
                logger.debug(f"'{msg_obj.msg}' Not a command..")
                continue

            # We have a 'command' - Lets try to Handle the command
            cmd, *args = msg_obj.msg.split()
            logger.debug(f"cmd: {cmd} args: {args}")
            cmd = cmd[1:]  # Remove command prefix
            msg_obj.cmd = cmd  # Added the command sent by the user to the msg_obj

            # Check if command has a function. If so command_handler is not the command function
            command_handler = self.commands[cmd]
            if command_handler:
                #logger.debug(f"Command '{cmd}' has handler func '{command_handler.__name__}'")
                msg_obj.cmd_args = args  # Every thing after <cmd prefix><cmd> is considered cmd arguments
                # Hack to reply to private messages
                if not msg_obj.channel.startswith("#"):
                    # Channel is always the 'target' when send_msg()
                    msg_obj.channel = f"{msg_obj.nick}"

                # Execute the command function
                if command_handler.is_function:
                    command_handler(msg=msg_obj, bot=self)
                else:
                    command_handler.input(msg=msg_obj, bot=self)

            else:
                # Received an unknown command
                self.send_msg(f"Unknown command. No command handlers for '{self.command_prefix + cmd}'",
                              target=msg_obj.channel)


