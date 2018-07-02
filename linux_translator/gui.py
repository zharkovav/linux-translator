# coding=utf-8
"""Pop-up window with word translation"""

import logging

from PySide import QtCore
from PySide import QtGui


logger = logging.getLogger('LT')


def docstring_style(text):
    """Format text as docstring"""
    return '<font style="color:#7fb95b">"""{}"""</font>'.format(text)


def header_style(text):
    """Format word as header"""
    header = '<font style="color:#a54926">Source word is: </font>' \
             '<font style="color:#5791a0">{}</font><br>'.format(text)
    return header


def word_with_error(text):
    """Format words with error"""
    word = '<font style="color:#b200b2">{}</font>'.format(text)
    return word


def word_suggest(text):
    """Format suggested words"""
    word = '<font style="color:#cc7832">{}</font>'.format(text)
    return word


class ScrollBar(QtGui.QScrollBar):
    """ScrollBar with custom vertical scrollbar"""
    def __init__(self, parent=None, **kwargs):
        QtGui.QScrollBar.__init__(self, parent, **kwargs)
        self.setStyleSheet(
            """
            /* VERTICAL */
            QScrollBar:vertical {
                border: none;
                background:  #2b2b2b;
                width: 8px;
                margin: 26px 0 26px 0;
            }

            QScrollBar::handle:vertical:hover {
                background: #ee875d;
                min-width: 26px;
            }

            QScrollBar::handle:vertical {
                background: #525252;
                min-height: 26px;
            }

            QScrollBar::add-line:vertical {
                background: none;
                height: 26px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                background: none;
                height: 26px;
                subcontrol-position: top left;
                subcontrol-origin: margin;
                position: absolute;
            }

            QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
                width: 26px;
                height: 26px;
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )


class QueueWorker(QtCore.QThread):
    """Queue thread"""
    update_signal = QtCore.Signal(dict)

    def __init__(self, queue=None, text_win=None, parent=None):
        super(QueueWorker, self).__init__(parent)
        self.queue = queue
        self.text_win = text_win
        self.stop = False

    def run(self):
        import Queue
        while not self.stop:
            try:
                data = self.queue.get_nowait()
                self.update_signal.emit(data)
            except Queue.Empty:
                continue

        logger.debug('Work thread is done. Exit.')


class PopupTranslate(QtGui.QWidget):
    """Popup window with translation"""

    def __init__(self, queue=None):
        super(PopupTranslate, self).__init__()
        self.text = None
        self.text_window = QtGui.QTextEdit(self)

        self.queue_thread = QueueWorker(queue=queue, text_win=self.text_window)

        self.queue_thread.start()

        self.queue_thread.update_signal.connect(self.update_ui)
        self.installEventFilter(self)
        self.init_popup_window()

    def exit(self):
        """Exit handler"""
        self.queue_thread.stop = True
        self.close()

    @QtCore.Slot(dict)
    def update_ui(self, data):
        """Slot for update pop-up window event"""
        logger.debug('Data recieved: %s', data)
        text = docstring_style(data.module_name)
        text += '<br>' + data.result + '<br>'
        self.text_window.append(text)

    def init_popup_window(self):
        """Init popup window"""
        widht = 450
        height = 250

        self.setWindowTitle('Linux Translator')
        self.text_window.setReadOnly(True)
        self.text_window.setWordWrapMode = False
        self.text_window.setVerticalScrollBar(ScrollBar(self))
        self.text_window.setStyleSheet(
            "QTextEdit {"
            "color: #a5b2c1;"
            "font-size: 14px;"
            "background-color: #2b2b2b;"
            "border: none;"
            "padding: 10px;"
            "}"
        )
        self.text_window.setGeometry(0, 0, widht, height)

    def show_popup(self, selection,  mouse_x, mouse_y):
        """Set window options and show it"""

        self.text_window.clear()
        self.text_window.activateWindow()
        self.text_window.append(header_style(selection))
        self.move(mouse_x, mouse_y)
        self.show()

    def eventFilter(self, widget, event):
        """Catch widget event and close window if Esc button pressed"""
        if event.type() == QtCore.QEvent.KeyPress and widget is self:
            key = event.key()
            if key == QtCore.Qt.Key_Escape:
                self.hide()
        return QtGui.QWidget.eventFilter(self, widget, event)

    def closeEvent(self, event):
        """Catch close event and just hide current window"""
        event.ignore()
        self.hide()
