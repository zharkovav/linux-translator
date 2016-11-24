"""Check spelling using yandex.ru service"""

import requests


def check_spelling(word):
    """Check spelling using Yandex api"""
    payload = {'text': word}
    resp = requests.get(
        "http://speller.yandex.net/services/spellservice.json/checkText",
        params=payload,
    )

    try:
        resp = resp.json()
    except Exception:
        pass
    return resp
