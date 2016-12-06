"""Main Application class"""

import os
import signal
import sys
from PySide import QtCore, QtGui

import gui
import keylistener
import lingualeo
import spellcheck


# pylint: disable=no-member
class App(QtGui.QApplication):
    """Rewrited QtGui.QApplication class"""
    sig_show = QtCore.Signal()
    sig_exit = QtCore.Signal()

    def __init__(self):
        super(App, self).__init__([])
        self.win = None

        # connect signals
        self.sig_show.connect(self.show_popup)
        self.sig_exit.connect(self.on_exit)

        # set action callbacks
        keylistener.action_callback = self.sig_show.emit
        keylistener.exit_callback = self.sig_exit.emit

        # start keyboard listener thread
        keylistener.new_hook.start()

    @staticmethod
    def get_selection():
        """Get current selection, translate it
        and return with current mouse position"""
        selection = os.popen('xsel').read()
        data = {}
        data.update(lingualeo.get_translate(selection))
        data.update(spellcheck.check_spelling(selection))
        x_pos = keylistener.new_hook.mouse_position_x
        y_pos = keylistener.new_hook.mouse_position_y
        return data, x_pos, y_pos

    @QtCore.Slot()
    def show_popup(self):
        """Show window with translate info"""
        data = self.get_selection()
        self.win = gui.PopupTranslate(*data)
        self.win.show()

    @QtCore.Slot()
    def on_exit(self):
        """Action on exit"""
        print 'Linux-translator applcation stopped.'
        self.closeAllWindows()
        keylistener.hook_exit()
        self.quit()


def main():
    """Main runner"""

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print 'Linux-translator applcation started. Use F2 to translate and ' \
          'F9 to exit (defaul values).'

    app = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
