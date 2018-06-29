"""Get word translate from lingualeo.com"""

import string
import re

import requests


def get_translate(word):
    """Translate word using Lingualeo api"""
    word = word.strip().strip(string.punctuation)
    # split under_scored words
    word = word.replace('_', ' ')

    # ToDo split CamelCase words
    # words = word.split()
    # for w in words:
    #     matches = re.finditer(
    #         '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
    #         w)
    #     print ' '.join([m.group(0) for m in matches])

    payload = {'word': word}

    trans = {
        'lingualeo': {
            "word": word,
            "error": (None, None),
            "twords": []
        }
    }

    try:
        resp = requests.get(
            "http://api.lingualeo.com/gettranslates",
            params=payload,
        )
        resp_json = resp.json()
        trans['lingualeo']['twords'] = (
            translation['value'].encode("utf-8")
            for translation in resp_json.get("translate", ())
        )
        trans['lingualeo']['error'] = (
            resp_json.get('error_code'),
            resp_json.get('error_msg'),
        )
    except requests.ConnectionError as err:
        trans['lingualeo']["error"] = (
            'Connection error occurred: {}'.format(err)
        )
    except Exception:
        trans['lingualeo']["error"] = (
            resp.status_code, resp.text.encode("utf-8"))
    return trans
