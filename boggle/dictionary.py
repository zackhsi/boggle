"""
This module contains a few options for representing the dictionary. They are
all lazily instantiated, and will not allocate any memory until called.

A dictionary fits perfectly well in memory (~10MB) for a list of words this
size. Tries are more fun though.
"""
from typing import Dict, Generator

import marisa_trie
import pygtrie

from boggle.settings import DICTIONARY_PATH, DICTIONARY_VARIANT

_dictionary: Dict[str, bool] = {}
_marisa_trie = None
_pygtrie = None


def words() -> Generator[str, None, None]:
    with open(DICTIONARY_PATH) as f:
        lines = f.readlines()
        for line in lines:
            yield line.strip()


def get_dictionary() -> Dict[str, bool]:
    global _dictionary
    if not _dictionary:
        for word in words():
            _dictionary[word] = True
    return _dictionary


def get_marisa_trie() -> marisa_trie.Trie:
    global _marisa_trie
    if not _marisa_trie:
        _marisa_trie = marisa_trie.Trie(words())
    return _marisa_trie


def get_pygtrie() -> pygtrie.CharTrie:
    global _pygtrie
    if not _pygtrie:
        _pygtrie = pygtrie.CharTrie()
        for word in words():
            _pygtrie[word] = True
    return _pygtrie


def lookup(word: str, *, variant: str = DICTIONARY_VARIANT) -> bool:
    result: bool
    if variant == 'dictionary':
        result = word in get_dictionary()
    elif variant == 'pygtrie':
        result = word in get_pygtrie()
    elif variant == 'marisa_trie':
        result = word in get_marisa_trie()
    else:
        raise ValueError(f'Unknown dictionary variant {DICTIONARY_VARIANT}')
    return result
