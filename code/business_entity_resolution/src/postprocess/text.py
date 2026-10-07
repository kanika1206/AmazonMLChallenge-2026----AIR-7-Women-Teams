import re

from unidecode import unidecode

ADDRESS_WORDS = {
    "st": "street", "rd": "road", "ave": "avenue", "av": "avenue", "dr": "drive", "ln": "lane",
    "blvd": "boulevard", "bd": "boulevard", "ct": "court", "pl": "place", "hwy": "highway",
    "pkwy": "parkway", "cir": "circle", "r": "rue", "rte": "route", "che": "chemin",
    "imp": "impasse", "fg": "faubourg", "sq": "square", "nr": "near", "opp": "opposite",
    "no": "", "n": "", "bis": "", "ter": "",
}


_NOT_ALPHANUMERIC = re.compile(r"[^a-z0-9 ]")


def _tokens(text):
    return _NOT_ALPHANUMERIC.sub(" ", text).split()


def address_tokens(address):
    words = (ADDRESS_WORDS.get(token, token) for token in _tokens(unidecode(address).lower()))
    return [word for word in words if word]


def normalize_address(address):
    return " ".join(address_tokens(address))


def name_key(name):
    text = unidecode(name).lower()
    text = text.replace("&", " and ").replace("+", " and ")
    return " ".join(_tokens(text))
