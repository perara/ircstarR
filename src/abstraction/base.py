from abc import ABC, abstractmethod
import inspect


class IRCcmd:
    """ Command decorator """

    @staticmethod
    def command(f):
        """ Decorator function """

        if inspect.isclass(f):
            f.is_function = False
        else:
            f.is_function = True

        f.__decorated__ = True
        return f


class CommandIFace(ABC):
    """ Interface for class based commands """

    @abstractmethod
    def cmd(self, msg, bot):
        """ All class based commands must implement 'cmd' func """
        raise NotImplementedError("You must implement this!")
