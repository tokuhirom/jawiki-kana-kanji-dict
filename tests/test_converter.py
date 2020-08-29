from jawiki.converter import Converter
import pytest

f = Converter()


@pytest.mark.parametrize("src,expected", [
    ('KEIYOGINKO POWER COUNTDOWN REAL', 'KEIYOGINKO POWER COUNTDOWN REAL'),
    ('阿坂城跡附 高城跡枳城跡', '阿坂城跡附高城跡枳城跡'),
    ('足利 右兵衛督 成氏', '足利右兵衛督成氏'),
    ('山田 太郎', '山田太郎'),
    ('がちりん&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;', 'がちりん'),
    ('I&amp;O', 'I&O'),
    ('&amp;epsilon;-&amp;delta;論法', 'ε-δ論法'),
    ('I&amp;#9829;OGI', 'I♥OGI'),
    ('赤&#x2123D;眞弓', '赤𡈽眞弓'),
    ('砂川奈美(旧姓:伊藤)', '砂川奈美'),
    ('篠宮慶子（本名：篠宮景子）', '篠宮慶子'),
])
def test_kanji_filter(src, expected):
    assert f.kanji_filter(src) == expected
