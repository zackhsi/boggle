import pytest
from pympler.asizeof import asizeof

from boggle import dictionary


@pytest.mark.parametrize(
    ('variant', 'word', 'expected_result'),
    [
        # Dictionary.
        ('dictionary', 'aardvark', True),
        ('dictionary', 'abcd', False),
        ('dictionary', '', False),
        # Marisa trie.
        ('marisa_trie', 'aardvark', True),
        ('marisa_trie', 'abcd', False),
        ('marisa_trie', '', False),
        # Pygtrie.
        ('pygtrie', 'aardvark', True),
        ('pygtrie', 'abcd', False),
        ('pygtrie', '', False),
    ]
)
def test_lookup(variant: str, word: str, expected_result: bool) -> None:
    result = dictionary.lookup(word, variant=variant)
    assert result == expected_result


def test_sizes() -> None:
    marisa_trie_size = asizeof(dictionary.get_marisa_trie())
    native_dictionary_size = asizeof(dictionary.get_dictionary())
    pygtrie_size = asizeof(dictionary.get_pygtrie())
    # marisa_trie_size is inaccurate due to its use of the MARISA c extension.
    # Properly profiling the trie size requires more work.  See
    # stackoverflow.com/questions/2615153/profiling-python-c-extensions.
    assert marisa_trie_size < native_dictionary_size < pygtrie_size
