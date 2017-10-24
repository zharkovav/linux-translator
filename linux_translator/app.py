"""Main Application class"""

import argparse
import os
import signal
import sys
import Queue

from PySide import QtCore
from PySide import QtGui

import config
import gui
import keylistener
import lingualeo
import spellcheck
import tray_indicator
import workers


# pylint: disable=no-member
class App(QtGui.QApplication):
    """Rewrited QtGui.QApplication class"""
    sig_show = QtCore.Signal()
    sig_exit = QtCore.Signal()

    def __init__(self):
        super(App, self).__init__([])
        self.win = None

        # get workers
        self.workers = workers.get_workers()
        self.data_queue = Queue.Queue()

        # connect signals
        self.sig_show.connect(self.show_popup)
        self.sig_exit.connect(self.on_exit)

        # set action callbacks
        keylistener.action_callback = self.sig_show.emit
        keylistener.exit_callback = self.sig_exit.emit

        # start keyboard listener thread
        keylistener.new_hook.start()

        # Initialise and show system tray icon
        self.tray_menu = tray_indicator.SystemTrayIcon(
            icon_file=os.path.join(
                os.path.dirname(__file__), "./tray-logo.png"
            ),
            exit_signal=self.sig_exit,
            menu_options=config.config['options'],
        )
        self.tray_menu.show()

    @staticmethod
    def get_selection():
        """Get current selection"""
        selection = os.popen('xsel').read()
        return selection

    @QtCore.Slot()
    def show_popup(self):
        """Show window with translate info"""
        selection = self.get_selection()

        for plugin in self.workers:
            mod = plugin(self.data_queue, selection)
            mod.start()

        print self.data_queue

        while not self.data_queue.empty():
            print 'Data: ', self.data_queue.get()

        data = {'src': selection}
        if config.config['options']['translation']:
            data.update(lingualeo.get_translate(selection))
        if config.config['options']['spellchecker']:
            data.update(spellcheck.check_spelling(selection))
        x_pos = keylistener.new_hook.mouse_position_x
        y_pos = keylistener.new_hook.mouse_position_y

        self.win = gui.PopupTranslate(data, x_pos, y_pos)
        self.win.show()

    @QtCore.Slot()
    def on_exit(self):
        """Action on exit"""
        print 'Linux-translator applcation stopped.'
        self.closeAllWindows()
        keylistener.hook_exit()
        self.quit()


def get_args():
    """ Read script arguments """
    parser = argparse.ArgumentParser(
        description='Linux-translator CLI interface.'
    )

    default_conf = os.path.join(os.path.dirname(__file__), 'config.json')

    parser.add_argument(
        "-c",
        dest="config_file",
        type=str,
        default=default_conf,
        help="JSON file with configuration"
    )

    args = parser.parse_args()

    return args


def main():
    """Main runner"""

    args = get_args()
    config.config.read(args.config_file)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print 'Linux-translator application started. Use F2 to translate and ' \
          'F9 to exit (default values).'

    app = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
