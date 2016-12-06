# coding=utf-8
"""Pop-up window with word translation"""

from PySide import QtGui, QtCore


def docstring_style(text):
    """Format text as docstring"""
    return '<font style="color:#7fb95b">"""{}"""<br></font>'.format(text)


def header_style(text):
    """Format word as header"""
    header = '<font style="color:#a54926">Source word is: </font>' \
             '<font style="color:#5791a0">{}</font><br><br>'.format(text)
    return header


def word_with_error(text):
    """Duck"""
    word = '<font style="color:#b200b2">{}</font>'.format(text)
    return word


def word_suggest(text):
    """Duck"""
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


class PopupTranslate(QtGui.QWidget):
    """Popup window with translation"""

    def __init__(self, data, mouse_x, mouse_y):
        super(PopupTranslate, self).__init__()

        self.text = None
        self.data = None
        self.text_window = None

        self.installEventFilter(self)
        self.show_popup(data, mouse_x, mouse_y)

    def show_popup(self, data, mouse_x, mouse_y):
        """Set window options and show it"""
        self.data = data

        self.get_text(data)

        widht = 450
        height = 250

        self.setGeometry(mouse_x, mouse_y, widht, height)

        self.setWindowTitle('Linux Translate')
        self.text_window = QtGui.QTextEdit(self.text, self)
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
        self.show()

    def get_text(self, data):
        """Duck"""
        trans = self.parse_translate(data)
        spell = self.parse_spellchecker(data)
        self.text = '<br><br>'.join((trans, spell))
        return self.text

    @staticmethod
    def parse_translate(data):
        """Create formatted text to display"""
        data = data['lingualeo']
        error = data.get('error')
        header = header_style(data['word'])
        if error:

            header += docstring_style('Lingualeo error')
            error = 'Error code - {}.<br>'.format(error[0])
            text = header + error
        else:
            header += docstring_style('Lingualeo translation')
            traslation = [
                '{}. {}'.format(idx, trans)
                for idx, trans in enumerate(data['twords'], start=1)
                ]
            text = header + '<br>'.join(traslation)

        text = text.decode('utf-8')
        return text

    @staticmethod
    def parse_spellchecker(data):
        """Parse Yandex spellchecker rusult"""
        data = data['yandex_speller']

        result_text = ''
        spell_checked_data = []
        point = 0
        for result in data['spellcheck']:
            start_sym = int(result['pos'])
            end_sym = start_sym + int(result['len'])

            before_error_word = data['word'][point:start_sym]
            spell_checked_data.append(before_error_word)

            src_word = word_with_error(data['word'][start_sym:end_sym])

            spell_checked_data.append(src_word)

            suggest_text = word_suggest('(' + ', '.join(result['s']) + ')')
            spell_checked_data.append(suggest_text)
            point = end_sym
        if point:
            spell_checked_data.append(data['word'][point:])

        spell_check_result = ''.join(spell_checked_data)
        if not spell_check_result:
            spell_check_result = 'No errors.'
        error = data.get('error')

        result_text += docstring_style('Spellchecker')
        if error:
            error = 'Error code - {}.<br>'.format(error[0])
            text = result_text + error
        else:
            text = result_text + '<br>' + spell_check_result

        text = text.decode('utf-8')
        return text

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
