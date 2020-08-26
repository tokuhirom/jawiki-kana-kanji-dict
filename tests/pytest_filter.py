import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawiki import filter


f = filter.WikipediaFilter()

def test_hojin_filter():
    kanji, yomi = f.hojin_filter('愛知県地方木材株式会社', 'あいちけんちほうもくざいかぶしきがいしゃ')
    assert kanji == '愛知県地方木材'
    assert yomi == 'あいちけんちほうもくざい'

def test_hojin_filter2():
    kanji, yomi = f.hojin_filter('愛知県地方木材株式会社', 'あいちけんちほうもくざい')
    assert kanji == '愛知県地方木材'
    assert yomi == 'あいちけんちほうもくざい'

