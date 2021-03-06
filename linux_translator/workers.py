import importlib
import inspect
import os

import modules.base

APP_NAME = 'linux_translator'
MOD_DIR = 'modules'


def get_module_class(mod):
    """Yield class object from given module"""
    for _, obj in inspect.getmembers(mod):
        if inspect.isclass(obj) and issubclass(obj, modules.base.BaseModule):
            yield obj


def get_workers():
    """Import modules, find worker classes and return list from them"""
    workers = []
    for mod in (
        mod_name
        for mod_name in os.listdir(
            os.path.join(
                os.path.dirname(__file__),
                MOD_DIR
            )
        )
        if (
            mod_name.endswith('.py') and
            mod_name != 'base.py' and
            not mod_name.startswith('__')
        )
    ):
        name, ext = os.path.splitext(mod)
        loaded_mod = importlib.import_module(
            '.'.join((APP_NAME, MOD_DIR, name))
        )
        workers.extend(list(get_module_class(loaded_mod)))
    return workers


if __name__ == '__main__':
    import Queue
    for m in get_workers():
        m(Queue.Queue()).start()
