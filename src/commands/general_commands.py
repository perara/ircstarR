from src.abstraction.base import CommandIFace, IRCcmd

import time
import logging

logger = logging.getLogger("ircstarr.gen_commands")


@IRCcmd.command(name="class_renamed")
class ClassWithAStupidName(CommandIFace):

    def __init__(self):
        pass

    def cmd(self, msg, bot):
        bot.send_msg("Original Class is %s!. Was renamed to %s." % (str(type(self)), self.name), target=msg.channel)


@IRCcmd.command
class ClassNamed(CommandIFace):

    def cmd(self, msg, bot):
        bot.send_msg("This class was not renamed and is called: %s." % (str(type(self))), target=msg.channel)


@IRCcmd.command
def fn_named(msg, bot):
    bot.send_msg("Called fn_named (The default name function)", target=msg.channel)


@IRCcmd.command(name="fn_renamed")
def fn_with_a_stupid_name(msg, bot):
    bot.send_msg("Called fn_renamed (NOT the default name function)", target=msg.channel)


# @IRCcmd.command
# def test_cmd2(msg, bot):
#     time.sleep(5)
#     bot.send_msg("test_cmd sleept for 5 sec", target=msg.channel)
#
#
# @IRCcmd.command
# def echo(msg, bot):
#     logger.info("echo() was called")
#     m = f"Command: {msg.cmd} Args: {' '.join(a for a in msg.cmd_args)}"
#     bot.send_msg(message=m, target=msg.channel)
#
#
# @IRCcmd.command
# def help(msg, bot):
#     logger.info("help() was called")
#     help_msg = "RTFM"
#     bot.send_private_msg(help_msg, nick=msg.nick)

# def channel_users(msg: Message, bot: IRC):
#     users = bot._send_cmd("who #starrbottest")
#     print("channel_users Response: ")
#     print(users)
