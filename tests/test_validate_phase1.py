
from jawiki import container
import pytest

c = container.Container()
f = c.get_filter()


@pytest.mark.parametrize("kanji,yomi,expected", [
    ('山田タロウ', 'やまだたろう', True),
    ('w3m', 'ダブリューサンエム または ダブリュースリーエム', False),
    ('3月', 'さんがつ', False),
    ('4004', 'よんまるまるよん', False),
    ('Keyboard / kAoru ikArAshi / 五十嵐 馨', 'いがらしかおる', False),
    ('ARIAの登場人物', 'ありあのとうじょうじんぶつ', False),
    ('アークライズファンタジアの登場キャラクター', 'あーくらいずふぁんたじあのとうじょうきゃらくたー', False),
    ('ウルトラQの登場怪獣', 'うるとらきゅーのとうじょうかいじゅう', False),
    ('仮面ライダー555の登場仮面ライダー', 'かめんらいだーふぁいずのとうじょうきゃらくたー', False),
    ('10.『七変化狸御殿』', 'しちへんげ たぬきごてん', False),
    ('第43話 - 第45話', 'ものくろ', False),
    ('キノミヤ信仰', 'しんこう', False),
    ('アイコナール近似', 'あいこなーるきんじ', True),
    ('アイム・キンキ理容美容専門学校', 'あいむきんきりようびようせんもんがっこう', True),
    ('本来はジョイスティック', 'あーけーどすてぃっく', False),
    ('谷本ヨーコ', 'たにもとようこ', True),
    ('You♡ I -Sweet Tuned by 5pb.-', 'ゆい', False),
])
def test_validate_phase2(kanji, yomi, expected):
    assert f.validate_phase2(kanji, yomi) == expected


@pytest.mark.parametrize("kanji,yomi,expected", [
    ('山田啓二', 'やまだけいじ', True),
    ('宇宙刑事魂 THE SPACE SHERIFF SPIRITS', 'うちゅうけいじたましい', False),
    ('愛植男', 'あいうえお', True),
    ('小林太志', 'こばやしふとし', True),
    ('旭丘中学校、旭ヶ丘中学校、旭が丘中学校', 'あさひがおかちゅうがっこう', False),
    ('御座船安宅丸', 'あたけまる', False),
    ('福岡市立内浜小学校', 'うちはましょうがっこう', False),
    ('東風汽車有限公司', 'とうふうきしゃ', False),
    ('山添村立奈良県立山辺高等学校山添分校', 'やまべこうとうがっこうやまぞえぶんこう', False),
    ('鷲谷いづみ', 'わしたにいずみ', True),
    ('飯山愛宕中継局', 'いいやまあたご', False),
])
def test_validate_phase3(kanji, yomi, expected):
    import sys
    got = f.validate_phase3(kanji, yomi)
    sys.stderr.write(str([kanji, yomi, got, expected]) + "\n")
    assert got == expected
