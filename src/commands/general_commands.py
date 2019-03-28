from src import add_handler
from src.abstraction.models import Message  # Only imported for intellisense reasons
from src.irc import IRC  # Only imported for intellisense reasons

import time
import logging

logger = logging.getLogger("ircstarr.gen_commands")


def test_cmd(msg, bot):
    print(f"msg: {msg} - bot: {bot}")


add_handler("test", test_cmd)


def test_cmd(msg: Message, bot: IRC):
    time.sleep(5)
    bot.send_msg("test_cmd sleept for 5 sec", target=msg.channel)


add_handler("testcmd", test_cmd)


def echo(msg: Message, bot: IRC):
    logger.info("echo() was called")
    m = f"Command: {msg.cmd} Args: {' '.join(a for a in msg.cmd_args)}"
    bot.send_msg(message=m, target=msg.channel)


add_handler("echo", echo)


def help(msg: Message, bot: IRC):
    logger.info("help() was called")
    help_msg = "RTFM"
    bot.send_private_msg(help_msg, nick=msg.nick)


add_handler("help", help)


# def channel_users(msg: Message, bot: IRC):
#     users = bot._send_cmd("who #starrbottest")
#     print("channel_users Response: ")
#     print(users)
