import pytest
from janome.tokenizer import Tokenizer

from jawiki.post_validate import PostValidator

tokenizer = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
f = PostValidator(tokenizer)


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
    msg = f.post_validate(kanji, yomi)
    print(msg)
    assert (msg is None) == expected


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
    ('倉知玲鳳', 'くらちれお', True),
    ('無限責任広部銀行', 'ひろべぎんこう', False),
    ('石包丁・石庖丁', 'いしぼうちょう', False),
    ('覚醒具・打出の大槌', 'うちでのおおづち', False),
    ('緒方三社川越し祭り', 'かわごしまつり', False),
    ('初井しづ枝', 'はついしずえ', True),
    ('おっぱいパブ', 'おっぱぶ', False),
    ('島野功緒', 'しまのいさお', True),
    ('前田怜緒', 'まえだれお', True),
    ('吉本玲緒', 'よしもとれお', True),
    ('湊川四良兵衞', 'みなとがわしろべえ', True),
    ('初井しづ枝', 'はついしづえ', True),
    ('福岡市立愛宕小学校', 'あたごしょうがっこう', False),
])
def test_validate_phase3(kanji, yomi, expected):
    msg = f.post_validate(kanji, yomi)
    got = msg is None
    print(str([kanji, yomi, msg, got, expected]) + "\n")
    assert got == expected
