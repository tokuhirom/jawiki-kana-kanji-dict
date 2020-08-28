import pytest

from jawiki import jachars


def test_is_kanji():
    assert jachars.is_kanji('KEIYOGINKO') == False
    assert jachars.is_kanji('粟飯原首胤度') == True


def test_is_hiragana():
    assert jachars.is_hiragana('めもり') == True
    assert jachars.is_hiragana('メモリ') == False
    assert jachars.is_hiragana('あいのめもりー') == True
    assert jachars.is_hiragana('KEIYOGINKO') == False


def test_is_katakana():
    assert jachars.is_katakana('メモリ') == True
    assert jachars.is_katakana('アイ・エム・アイ') == False
    assert jachars.is_katakana('KEIYOGINKO') == False


@pytest.mark.parametrize("s,p", [
    ('ひ', 'い'),
    ('あゝ', 'ああ'),
    ('いすゞ', 'いすず'),
    ('へる', 'える'),
])
def test_normalize_hiragana(s, p):
    assert jachars.normalize_hiragana(s) == jachars.normalize_hiragana(p)
