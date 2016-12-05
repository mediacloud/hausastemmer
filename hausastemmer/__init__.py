from hausastemmer.HausaStemmer import HausaStemmer

# noinspection PyRedundantParentheses
__all__ = ('stem')

__stemmer = HausaStemmer()


def stem(term, lookup=True):
    # type: (str, bool) -> str
    """Stem Hausa language term (word).
    :param term: term (word) to stem
    :param lookup: whether to use lookup dictionary for stemming
    :return: stemmed term, or original term if the term can't be stemmed
    :rtype: str
    """

    # FIXME maybe trim the stem?
    # FIXME remove len()
    # FIXME implement lookup()
    # FIXME add tests with empty / random / bad data
    term_stem = __stemmer.stem(p=term, lookup=lookup)

    return term_stem
