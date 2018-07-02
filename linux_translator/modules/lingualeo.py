"""Module uses Lingualeo API to translate selected text.
This module split under_scored words and CamelCase words.
"""

import collections
import logging
import re
import string
import threading

import requests

import base
from .. import config


class Translate(
        collections.namedtuple(
            'Translate',
            (
                'selection',
                'error',
                'twords',
            )
        )
):
    """Class container to store traslation result"""
    __slots__ = ()


class LingualeoTranslate(base.BaseModule):
    """LinguaLeo translator worker"""

    NAME = 'Lingualeo translation'

    def get_translate(self):
        """Translate selection using Lingualeo api"""
        selection = self.selection.strip().strip(string.punctuation)
        selection = selection.replace('_', ' ')

        # ToDo split CamelCase words
        words = selection.split()
        splitted = []
        for w in words:
            matches = re.finditer(
                '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
                w)
            splitted.append(' '.join([m.group(0) for m in matches]))
        selection = ' '.join(splitted)

        payload = {'word': selection}

        twords = []
        try:
            resp = requests.get(
                "http://api.lingualeo.com/gettranslates",
                params=payload,
            )
            resp_json = resp.json()
            twords = [
                translation['value'].encode("utf-8")
                for translation in resp_json.get("translate", ())
            ]
            error = resp_json.get('error_msg')
        except requests.ConnectionError as err:
            error = 'Connection error occurred: {}'.format(err)
        except ValueError:
            error = resp.text.encode("utf-8")
        except Exception as err:
            error = 'Error occurred in translator module: {}'.format(err)

        res = Translate(
            selection=selection,
            error=error or None,
            twords=twords,
        )
        return res

    @staticmethod
    def format_translate(data):
        """Create formatted text to display"""
        if data.error:
            error = 'Error in translation module: {}.<br>'.format(
                repr(data.error)
            )
            text = error
        else:
            traslation = [
                '{}. {}'.format(idx, trans)
                for idx, trans in enumerate(data.twords, start=1)
                ]
            text = '<br>'.join(traslation)

        text = text.decode('utf-8')
        return text

    def run(self):
        """Get translation of selected text, format it and return back."""
        if config.config['options']['translation']:
            logger = logging.getLogger('LT')
            logger.debug(
                '%s: module started in new thread: %s',
                self.NAME,
                threading.current_thread()
            )

            translate = self.get_translate()
            formatted = self.format_translate(translate)
            res = base.Result(
                module_name=self.NAME,
                result=formatted,
            )
            self.queue.put(res)
            logger.debug('%s: Put data in queue: %s', self.NAME, res)
