"""This module contains System tray icon with application menu"""

import functools

from PySide import QtCore
from PySide import QtGui

import config


class AppTrayMenu(QtGui.QMenu):
    """Class represent applicacion tray menu"""

    def __init__(self, options, parent=None):
        QtGui.QMenu.__init__(self, parent)

        self.actions = []
        self.options = options
        self.construct_actions()
        self.addSeparator()
        self.exit_action = self.addAction("Exit")

    def construct_actions(self):
        """Create actions from config options and add to menu"""
        for key, value in self.options.iteritems():
            action = self.addAction(key)
            action.setCheckable(True)
            self.connect(
                action, QtCore.SIGNAL('triggered()'),
                functools.partial(self.handle_option_action, key),
            )
            if value:
                action.setChecked(True)

    def handle_option_action(self, opt_name):
        """Enable or disable action option"""
        config.config['options'][opt_name] = not config.config['options'][opt_name]


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    """Class to construct and control application tray icon"""

    def __init__(self, icon_file, exit_signal, menu_options={}, parent=None):
        icon = QtGui.QIcon(icon_file)
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.on_exit = exit_signal
        menu = AppTrayMenu(menu_options, parent)
        self.setContextMenu(menu)
        self.connect(menu.exit_action, QtCore.SIGNAL('triggered()'), self.exit)

    def exit(self):
        """This method trigger on_exit signal"""
        self.on_exit.emit()
