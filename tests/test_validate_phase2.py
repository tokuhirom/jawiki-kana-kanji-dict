from jawiki import filter
import pytest
import logging


# TODO parameterize
def test_validate_phase2():
    f = filter.WikipediaFilter()

    assert f.validate_phase2('山田タロウ', 'やまだたろう') == True

    assert f.validate_phase2('w3m', 'ダブリューサンエム または ダブリュースリーエム') == False
    assert f.validate_phase2('3月', 'さんがつ') == False
    assert f.validate_phase2('4004', 'よんまるまるよん') == False
    assert f.validate_phase2('Keyboard / kAoru ikArAshi / 五十嵐 馨', 'いがらしかおる') == False
    assert f.validate_phase2('ARIAの登場人物', 'ありあのとうじょうじんぶつ') == False
    assert f.validate_phase2('アークライズファンタジアの登場キャラクター', 'あーくらいずふぁんたじあのとうじょうきゃらくたー') == False
    assert f.validate_phase2('ウルトラQの登場怪獣', 'うるとらきゅーのとうじょうかいじゅう') == False
    assert f.validate_phase2('仮面ライダー555の登場仮面ライダー', 'かめんらいだーふぁいずのとうじょうきゃらくたー') == False
    assert f.validate_phase2('10.『七変化狸御殿』', 'しちへんげ たぬきごてん') == False
    assert f.validate_phase2('第43話 - 第45話', 'ものくろ') == False
    assert f.validate_phase2('キノミヤ信仰', 'しんこう') == False
    assert f.validate_phase2('アイコナール近似', 'あいこなーるきんじ') == True
    assert f.validate_phase2('アイム・キンキ理容美容専門学校', 'あいむきんきりようびようせんもんがっこう') == True


def test_validate_phase2_postfix():
    f = filter.WikipediaFilter()
    assert f.validate_phase2('本来はジョイスティック', 'あーけーどすてぃっく') == False
    assert f.validate_phase2('谷本ヨーコ', 'たにもとようこ') == True
    assert f.validate_phase2('You♡ I -Sweet Tuned by 5pb.-', 'ゆい') == False


logging.basicConfig(level=logging.DEBUG)

f = filter.WikipediaFilter(logger=logging.getLogger())


@pytest.mark.parametrize("kanji,yomi,expected", [
    ('山田啓二', 'やまだけいじ', True),
    ('宇宙刑事魂 THE SPACE SHERIFF SPIRITS', 'うちゅうけいじたましい', False),
    ('愛植男', 'あいうえお', True),
    ('小林太志', 'こばやしふとし', True),
    ('旭丘中学校、旭ヶ丘中学校、旭が丘中学校', 'あさひがおかちゅうがっこう', False),
])
def test_validate_phase3(kanji, yomi, expected):
    assert f.validate_phase3(kanji, yomi) == expected

