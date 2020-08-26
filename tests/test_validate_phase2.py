import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jawiki import filter

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

