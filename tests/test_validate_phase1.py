
from jawiki import filter
import pytest

f = filter.WikipediaFilter()


@pytest.mark.parametrize("title,kanji,yomi,expected", [
    ('a', '又八郎', 'またはちろう', True),
    ('a', 'アクメスジト', 'またはあくめちぇっと', False),
    ('a', 'マタハリ百貨店', 'またはりひゃっかてん', True),
    ('a', 'イルーニャ', 'または', False),
])
def test_validate_phase1(title, kanji, yomi, expected):
    assert f.validate_phase1(title, kanji, yomi) == expected
