"""Check spelling using yandex.ru service"""

import requests


def check_spelling(word):
    """Check spelling using Yandex api"""
    payload = {'text': word}
    resp = requests.get(
        "http://speller.yandex.net/services/spellservice.json/checkText",
        params=payload,
    )

    checker = {
        'yandex_speller': {
            "word": word,
            "error": None,
            "spellcheck": [],
        }
    }

    try:
        resp = resp.json()
        checker['yandex_speller']['spellcheck'] = resp
    except Exception:
        checker['yandex_speller']["error"] = (
            resp.status_code, resp.text.encode("utf-8"))
    return checker
