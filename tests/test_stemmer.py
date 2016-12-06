# coding=utf-8

# Copyright (C) 2013 Bimba Andrew Thomas, 2016 Linas Valiukas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details <http://www.gnu.org/licenses/>.


from hausastemmer import stem
from .ref_stems.with_dict_lookup import TEST_STEMS_WITH_DICT_LOOKUP
from .ref_stems.without_dict_lookup import TEST_STEMS_WITHOUT_DICT_LOOKUP


def test_stemmer_with_bad_data():
    assert stem('') == ''
    assert stem('ą') == 'ą'

    # Won't necessarily return the same string
    assert len(stem('ą' * 1024 * 1024)) > 1024 * 1023


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
