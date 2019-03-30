import functools
from abc import ABC, abstractmethod
import inspect


class IRCcmd:
    """ Command decorator """

    @staticmethod
    def command(f=None, **kwargs):
        """ Decorator function """

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f = args[0]

            if "name" in kwargs:
                print(f, "setting name to", kwargs["name"])
                f.name = kwargs["name"]
            else:
                f.name = f.__name__
                print(f, "has name", f.name)
            f.is_function = not inspect.isclass(f)
            f.__decorated__ = True

            return f

        if f is None:
            return functools.partial(wrapper, **kwargs)

        wrapper(f, kwargs)
        return f

#f.is_function = not inspect.isclass(f)
#f.__decorated__ = True

class CommandIFace(ABC):
    """ Interface for class based commands """

    @abstractmethod
    def cmd(self, msg, bot):
        """ All class based commands must implement 'cmd' func """
        raise NotImplementedError("You must implement this!")
