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

    NAME = 'Base'

    def __init__(self, queue, selection=''):
        """Initialisation method. Store selection string to instance."""
        super(BaseModule, self).__init__()
        self.selection = selection
        self.queue = queue

    def run(self):
        """Run module processing. Should be implemented in child classes."""
        raise NotImplemented
