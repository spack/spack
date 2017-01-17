import sys

class Std(object):
    """ makes top-level python modules available as an attribute,
        importing them on first access.
    """

    def __init__(self):
        self.__dict__ = sys.modules

    def __getattr__(self, name):
        try:
            m = __import__(name)
        except ImportError:
            raise AttributeError("py.std: could not import %s" % name)
        return m

std = Std()
