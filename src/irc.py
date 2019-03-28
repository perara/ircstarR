import logging
import socket
import ssl
import time
import re


logger = logging.getLogger("ircstarr.irc")


class IRC:
    """ Class for handling all the IRC specific stuff """

    def __init__(self, server, port, use_ssl, channel, bot_nick, bot_owner, username, password="", command_prefix="."):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.channel = channel
        self.bot_nick = bot_nick
        self.bot_owner = bot_owner

        self.exitcode = "bye " + self.bot_nick

        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.command_prefix = command_prefix
        self.message_pattern = \
            re.compile(r":(?P<nick>\w+)!(?P<username>.+)\@(?P<userhost>.+) (?P<server_cmd>[A-Z]+) (?P<channel>(#?)\w+) :(?P<msg>.+)\r\n")

        self.isConnected = False

    def _connect(self):
        """ Connect to IRC server """

        if self.use_ssl:
            logger.debug("Using SSL")
            self.ircsock = ssl.wrap_socket(self.ircsock)

        self.ircsock.connect((self.server, self.port))

        if self.password:
            # Authenticate
            logger.debug("Using password authentication")
            self.ircsock.send(bytes(f"PASS {self.password}\n", "UTF-8"))

        self.ircsock.send(
            bytes(f"USER {self.username} {self.username} {self.username} :{self.bot_nick}\n", "UTF-8"))
        self.ircsock.send(bytes(f"NICK  {self.bot_nick}\n", "UTF-8"))

        self.isConnected = True
        logger.info("Connected I guess")

    def _pong(self):
        """" Respond to server Pings """
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
        logger.debug("Sent PONG to server")

    def _join_channel(self):
        """ Join channel """

        self.ircsock.send(bytes(f"JOIN {self.channel}\n", "UTF-8"))

        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            if ircmsg: logger.info(repr(ircmsg))

        logger.info(f"Joined channel {self.channel} as {self.bot_nick}")

    def send_msg(self, message: str, target: str):
        """ Send 'PRIVMSG' to target ex channel or a user """
        self.ircsock.send(bytes(f"PRIVMSG {target} :{message}\n", "UTF-8"))
        logger.info(f"Sent message '{message}' to '{target}'")

    def send_private_msg(self, message: str, nick: str):
        """ Send a private message """
        self.send_msg(message, nick)

    def _send_cmd(self, command: str):
        """ Execute a 'irc server' command """
        # Command must be the "raw" irc command to execute
        logger.debug(f"Executing command '{command}'")
        self.ircsock.send(bytes(f"{command}\n", "UTF-8"))
        response = []
        ircmsg = ""
        while ircmsg.find("End of /WHO list.") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            logger.debug(repr(ircmsg))
            response.append(ircmsg)

        return response

