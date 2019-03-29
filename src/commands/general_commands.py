from src.abstraction.base import BaseIFace, IRC

import time
import logging

logger = logging.getLogger("ircstarr.gen_commands")


@IRC.command
class testing(BaseIFace):

    def __init__(self):
        pass

    def input(self, msg, bot):
        bot.send_msg("PIM PAM POM!", target=msg.channel)


@IRC.command
def test_cmd1(msg, bot):
    print(f"msg: {msg} - bot: {bot}")


@IRC.command
def test_cmd2(msg, bot):
    time.sleep(5)
    bot.send_msg("test_cmd sleept for 5 sec", target=msg.channel)


@IRC.command
def echo(msg, bot):
    logger.info("echo() was called")
    m = f"Command: {msg.cmd} Args: {' '.join(a for a in msg.cmd_args)}"
    bot.send_msg(message=m, target=msg.channel)


@IRC.command
def help(msg, bot):
    logger.info("help() was called")
    help_msg = "RTFM"
    bot.send_private_msg(help_msg, nick=msg.nick)

# def channel_users(msg: Message, bot: IRC):
#     users = bot._send_cmd("who #starrbottest")
#     print("channel_users Response: ")
#     print(users)
