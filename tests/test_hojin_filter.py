import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawiki.hojin import hojin_filter

@pytest.mark.parametrize("kanji,kana,expected_kanji,expected_kana", [
    ('愛知県地方木材株式会社', 'あいちけんちほうもくざいかぶしきがいしゃ', '愛知県地方木材', 'あいちけんちほうもくざい'),
    ('愛知県地方木材株式会社', 'あいちけんちほうもくざい', '愛知県地方木材', 'あいちけんちほうもくざい'),
    ('株式会社少年画報社', 'しょうねんがほうしゃ', '少年画報社', 'しょうねんがほうしゃ'),
    ('京浜急行電鉄株式会社', 'けいひんきゅうこうでんてつ', '京浜急行電鉄', 'けいひんきゅうこうでんてつ'),
    ('アイパック', 'あいぱっくかぶしきかいしゃ', 'アイパック', 'あいぱっく'),
    ('国立研究開発法人宇宙航空研究開発機構', 'うちゅうこうくうけんきゅうかいはつきこう', '宇宙航空研究開発機構', 'うちゅうこうくうけんきゅうかいはつきこう'),
    ('国立研究開発法人', 'こくりつけんきゅうかいはつほうじん', '国立研究開発法人', 'こくりつけんきゅうかいはつほうじん'),
])
def test_hojin_filter(kanji, kana, expected_kanji, expected_kana):
    kanji, yomi = hojin_filter(kanji, kana)
    assert kanji == expected_kanji
    assert yomi == expected_kana

