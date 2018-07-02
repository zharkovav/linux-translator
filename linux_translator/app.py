"""Main Application class"""

import argparse
import logging
import os
import Queue
import signal
import sys

from PySide import QtCore
from PySide import QtGui

import config
import gui
import keylistener
import tray_indicator
import workers


# create logger
logger = logging.getLogger('LT')


def setup_logger(level=logging.INFO):
    """Setup logger configuration"""
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter(
        '[%(asctime)s][%(levelname)-5s][%(filename)-15s:%(lineno)3d] %(message)s'
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # Log level colors
    logging.addLevelName(logging.DEBUG, "\033[34m{}\033[0m".format(logging.getLevelName(logging.DEBUG)))
    logging.addLevelName(logging.INFO, "\033[32m{}\033[0m".format(logging.getLevelName(logging.INFO)))
    logging.addLevelName(logging.WARNING, "\033[33m{}\033[0m".format(logging.getLevelName(logging.WARNING)))
    logging.addLevelName(logging.ERROR, "\033[31m{}\033[0m".format(logging.getLevelName(logging.ERROR)))
    logging.addLevelName(logging.CRITICAL, "\033[41m{}\033[0m".format(logging.getLevelName(logging.CRITICAL)))

    # add ch to logger
    logger.addHandler(ch)


# pylint: disable=no-member
class App(QtGui.QApplication):
    """Rewrited QtGui.QApplication class"""
    sig_show = QtCore.Signal()
    sig_exit = QtCore.Signal()

    def __init__(self):
        super(App, self).__init__([])

        # get workers
        self.workers = workers.get_workers()
        self.data_queue = Queue.Queue()

        self.win = gui.PopupTranslate(self.data_queue)

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

        x_pos = keylistener.new_hook.mouse_position_x
        y_pos = keylistener.new_hook.mouse_position_y

        self.win.show_popup(selection, x_pos, y_pos)

    @QtCore.Slot()
    def on_exit(self):
        """Action on exit"""
        self.win.exit()
        self.closeAllWindows()
        self.quit()
        logger.info('Linux-translator applcation stopped.')
        keylistener.hook_exit()


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
    parser.add_argument(
        "-d",
        "--debug",
        action='store_true',
        help="Enable logger debug mode"
    )

    args = parser.parse_args()

    return args


def main():
    """Main runner"""

    args = get_args()
    config.config.read(args.config_file)

    level = logging.DEBUG if args.debug else logging.INFO
    setup_logger(level)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    logger.info(
        'Linux-translator application started. Use F2 to translate and '
        'F9 to exit (default values).'
    )

    app = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
