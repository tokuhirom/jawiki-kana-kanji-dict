from jawiki import filter

f = filter.WikipediaFilter()


def test_kanji_filter():
    assert f.kanji_filter('KEIYOGINKO POWER COUNTDOWN REAL') == 'KEIYOGINKO POWER COUNTDOWN REAL'
    assert f.kanji_filter('阿坂城跡附 高城跡枳城跡') == '阿坂城跡附高城跡枳城跡'
    assert f.kanji_filter('足利 右兵衛督 成氏') == '足利右兵衛督成氏'
    assert f.kanji_filter('山田 太郎') == '山田太郎'


def test_basic_filter():
    assert f.basic_filter('がちりん&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;') == 'がちりん'
    assert f.basic_filter('I&amp;O') == 'I&O'
    assert f.basic_filter('&amp;epsilon;-&amp;delta;論法') == 'ε-δ論法'
    assert f.basic_filter('I&amp;#9829;OGI') == 'I♥OGI'
    assert f.basic_filter('赤&#x2123D;眞弓') == '赤𡈽眞弓'
    assert f.basic_filter('砂川奈美(旧姓:伊藤)') == '砂川奈美'
    assert f.basic_filter('篠宮慶子（本名：篠宮景子）') == '篠宮慶子'
