import base
import threading


class LingualeoTranslate(base.BaseModule):
    """LinguaLeo translator worker"""

    NAME = 'LinguaLeo'

    def run(self, selection=None):
        print 'Run Lingualeo translation Thread: ', threading.current_thread()
