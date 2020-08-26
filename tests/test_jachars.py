import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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

