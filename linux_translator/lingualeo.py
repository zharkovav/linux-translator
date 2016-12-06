"""Get word translate from lingualeo.com"""

import string

import requests


def get_translate(word):
    """Translate word using Lingualeo api"""
    word = word.strip().strip(string.punctuation)
    payload = {'word': word}
    resp = requests.get(
        "http://api.lingualeo.com/gettranslates",
        params=payload,
    )

    trans = {
        'lingualeo': {
            "word": word,
            "error": None,
        }
    }

    try:
        resp = resp.json()
        trans['lingualeo']["twords"] = (
            trans['value'].encode("utf-8")
            for trans in resp["translate"]
        )
    except Exception:
        trans['lingualeo']["error"] = (
            resp.status_code, resp.text.encode("utf-8"))
    return trans
