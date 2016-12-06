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


from hausastemmer.HausaStemmer import HausaStemmer
import hausastemmer.__about__

# noinspection PyRedundantParentheses
__all__ = ('__version__', 'stem')

__version__ = __about__.__version__

__stemmer = HausaStemmer()


def stem(term, lookup=True):
    # type: (str, bool) -> str
    """Stem Hausa language term (word).
    :param term: term (word) to stem
    :param lookup: whether to use lookup dictionary for stemming
    :return: stemmed term, or original term if the term can't be stemmed
    :rtype: str
    """

    term = term.strip()

    # FIXME remove len()
    # FIXME implement lookup()
    # FIXME add tests with empty / random / bad data
    term_stem = __stemmer.stem(p=term, lookup=lookup)

    return term_stem
