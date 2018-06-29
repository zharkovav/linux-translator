"""Check spelling using yandex.ru service"""

import requests


def check_spelling(word):
    """Check spelling using Yandex api"""
    payload = {'text': word}

    checker = {
        'yandex_speller': {
            "word": word,
            "error": None,
            "spellcheck": [],
        }
    }

    try:
        resp = requests.get(
            "http://speller.yandex.net/services/spellservice.json/checkText",
            params=payload,
        )
        resp = resp.json()
        checker['yandex_speller']['spellcheck'] = resp
    except requests.ConnectionError as err:
        checker['yandex_speller']["error"] = (
            'Connection error occurred: {}'.format(err)
        )
    except Exception:
        checker['yandex_speller']["error"] = (
            resp.status_code, resp.text.encode("utf-8"))
    return checker
