import base
import threading


class YandexSpellcheck(base.BaseModule):
    """Yandex spellchecker worker"""

    NAME = "Yandex Spellchecker"

    def run(self, selection=None):
        print 'Run Yandex spellchecker. Thread: ', threading.current_thread()
