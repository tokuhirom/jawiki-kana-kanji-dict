import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawiki import filter

def test_validate_phase1():
    f = filter.WikipediaFilter()

    assert f.validate_phase1('a', '又八郎', 'またはちろう') == True
    assert f.validate_phase1('a', 'アクメスジト', 'またはあくめちぇっと') == False
    assert f.validate_phase1('a', 'マタハリ百貨店', 'またはりひゃっかてん') == True
    assert f.validate_phase1('a', 'イルーニャ', 'または') == False

