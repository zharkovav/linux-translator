import collections
import threading


class Result(
        collections.namedtuple(
            'Result',
            (
                'module_name',
                'result',
            )
        )
):
    """Class container for result object."""
    __slots__ = ()


class BaseModule(threading.Thread):
    """Base class for all modules"""

    def run(self, selection=None):
        raise NotImplemented
