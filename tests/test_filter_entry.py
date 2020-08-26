import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawiki import filter


f = filter.WikipediaFilter()

testdata = []
with open('tests/mapping.tsv', 'r') as fp:
    for line in fp:
        testdata.append(line.strip().split("\t"))

@pytest.mark.parametrize("input_title,input_kana,input_yomi,expected_kanji,expected_yomi", testdata)
def test_tsv(input_title, input_kana, input_yomi, expected_kanji, expected_yomi):
    got_kanji, got_yomi = f.filter_entry(input_title, input_kana, input_yomi)
    assert got_kanji == expected_kanji
    assert got_yomi == expected_yomi

