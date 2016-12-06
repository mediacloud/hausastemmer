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


"""
Hausa language stemmer reference implementation by Bimba et al., 2015. Uses Hausa affix-rules
and reference lookup to stem words in Hausa language.

Paper: Bimba, A., Idris, N., Khamis, N. and Noor, N.F.M. (2015) ‘Stemming Hausa text: Using affix-stripping rules and
reference look-up’, Language Resources and Evaluation, 50(3), pp. 687–703. doi: 10.1007/s10579-015-9311-x.
URL: https://bit.ly/hausa-stemming-bimba.

Based on modifications to the implementation of the Porter's Stemming Algorithm by Vivake Gupta (2001).

Copyright (C) 2013 Bimba Andrew Thomas <andrewbimba@gmail.com>, Department of Artificial Intelligence,
FSKTM Universiti Malaya, Kuala Lumpur, Malaysia.

Adapted as a Python module by Linas Valiukas <lvaliukas@cyber.law.harvard.edu>.
"""

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

    term_stem = __stemmer.stem(p=term, lookup=lookup)

    return term_stem
