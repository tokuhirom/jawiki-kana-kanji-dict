import pytest

from jawiki import jachars


@pytest.mark.parametrize("s,expected", [
    ('KEIYOGINKO', False),
    ('粟飯原首胤度', True),
])
def test_is_kanji(s, expected):
    assert jachars.is_kanji(s) == expected


@pytest.mark.parametrize("s,expected", [
    ('めもり', True),
    ('メモリ', False),
    ('あいのめもりー', True),
    ('KEIYOGINKO', False),
])
def test_is_hiragana(s, expected):
    assert jachars.is_hiragana(s) == expected


@pytest.mark.parametrize("s,expected", [
    ('メモリ', True),
    ('アイ・エム・アイ', False),
    ('KEIYOGINKO', False),
])
def test_is_katakana(s, expected):
    assert jachars.is_katakana(s) == expected


@pytest.mark.parametrize("s,p", [
    ('ひ', 'い'),
    ('あゝ', 'ああ'),
    ('いすゞ', 'いすず'),
    ('へる', 'える'),
    ('いずみ', 'いづみ'),
])
def test_normalize_hiragana(s, p):
    assert jachars.normalize_hiragana(s) == jachars.normalize_hiragana(p)
