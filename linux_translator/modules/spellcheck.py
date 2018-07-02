import collections
import logging
import requests
import string
import threading

from .. import config

import base


class SpellCheckResult(
        collections.namedtuple(
            'SpellCheckResult',
            (
                'selection',
                'error',
                'spellcheck',
            )
        )
):
    """Class container to store spell checker result"""
    __slots__ = ()


class YandexSpellcheck(base.BaseModule):
    """Yandex spellchecker worker"""

    NAME = "Yandex Spellchecker"

    def get_spellcheck(self):
        selection = self.selection.strip().strip(string.punctuation)
        payload = {'text': selection}

        resp = ''
        try:
            resp = requests.get(
                "http://speller.yandex.net/services/spellservice.json/checkText",
                params=payload,
            )
            resp = resp.json()
            error = None
        except requests.ConnectionError as err:
            error = 'Connection error occurred: {}'.format(err)
        except Exception as err:
            error = str(resp.status_code) + resp.text.encode("utf-8")

        result = SpellCheckResult(
            selection=selection,
            error=error,
            spellcheck=resp,
        )

        return result

    @staticmethod
    def format_word_with_error(text):
        """Format words with error"""
        word = '<font style="color:#b200b2">{}</font>'.format(text)
        return word

    @staticmethod
    def format_word_suggest(text):
        """Format suggested words"""
        word = '<font style="color:#cc7832">{}</font>'.format(text)
        return word

    def format_result(self, data):
        """Format spellchecker result"""

        result_text = ''
        spell_checked_data = []
        point = 0
        for result in data.spellcheck:
            start_sym = int(result['pos'])
            end_sym = start_sym + int(result['len'])

            before_error_word = data.selection[point:start_sym]
            spell_checked_data.append(before_error_word)

            src_word = self.format_word_with_error\
                (data.selection[start_sym:end_sym]
                 )

            spell_checked_data.append(src_word)

            suggest_text = self.format_word_suggest(
                ' ({})'.format(', '.join(result['s']))
            )
            spell_checked_data.append(suggest_text)
            point = end_sym
        if point:
            spell_checked_data.append(data.selection[point:])

        spell_check_result = (
            ''.join(spell_checked_data)
            if spell_checked_data
            else 'No errors.'
        )

        error = data.error
        if error:
            error = 'Error - {}.<br>'.format(error)
            text = result_text + error
        else:
            text = result_text + spell_check_result

        text = text.decode('utf-8')
        return text

    def run(self, selection=None):
        """Run module process"""
        if config.config['options']['spellchecker']:
            logger = logging.getLogger('LT')
            logger.debug(
                '%s: module started in new thread: %s',
                self.NAME,
                threading.current_thread()
            )

            spellcheck = self.get_spellcheck()
            formatted = self.format_result(spellcheck)

            res = base.Result(
                module_name=self.NAME,
                result=formatted,
            )
            self.queue.put(res)
            logger.debug('%s: Put data in queue: %s', self.NAME, res)
