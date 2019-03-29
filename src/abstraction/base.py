import abc
import inspect

class IRC:

    @staticmethod
    def command(f):

        if inspect.isclass(f):
            f.is_function = False
        else:
            f.is_function = True

        f.__decorated__ = True
        return f


class BaseIFace(abc.ABC):

    def input(self, msg, bot):
        raise NotImplementedError("You must implement this!")
