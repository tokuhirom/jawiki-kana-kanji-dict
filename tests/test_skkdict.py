from jawiki import skkdict


def test_merge_skkdict():
    assert skkdict.merge_skkdict([{'a': ['b'], 'c':['d']}, {'c': ['f'], 'd':['3']}]) == \
        {'a': ['b'], 'c': ['d', 'f'], 'd': ['3']}
