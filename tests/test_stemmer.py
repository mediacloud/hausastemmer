from hausastemmer import stem
from .ref_stems.with_dict_lookup import TEST_STEMS_WITH_DICT_LOOKUP
from .ref_stems.without_dict_lookup import TEST_STEMS_WITHOUT_DICT_LOOKUP


def test_stemmer_with_dict_lookup():
    for term, expected_stem in sorted(TEST_STEMS_WITH_DICT_LOOKUP.items()):
        actual_stem = stem(term, lookup=True)
        if expected_stem != actual_stem:
            print("Testing '%s' with dictionary lookup, expecting to get '%s', got '%s'" %
                  (term, expected_stem, actual_stem))
        assert actual_stem == expected_stem


def test_stemmer_without_dict_lookup():
    for term, expected_stem in sorted(TEST_STEMS_WITHOUT_DICT_LOOKUP.items()):
        actual_stem = stem(term, lookup=False)
        if expected_stem != actual_stem:
            print("Testing '%s' without dictionary lookup, expecting to get '%s', got '%s'" %
                  (term, expected_stem, actual_stem))
        assert actual_stem == expected_stem
