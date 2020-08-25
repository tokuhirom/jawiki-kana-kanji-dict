import unittest
from jawiki import filter

class TestWikipediaFilter(unittest.TestCase):

    def test_is_kanji(self):
        self.assertEqual(filter.is_kanji('粟飯原首胤度'), True)

    def test_is_hiragana(self):
        self.assertEqual(filter.is_hiragana('めもり'), True)
        self.assertEqual(filter.is_hiragana('メモリ'), False)
        self.assertEqual(filter.is_hiragana('あいのめもりー'), True)

    def test_is_katakana(self):
        self.assertEqual(filter.is_katakana('メモリ'), True)
        self.assertEqual(filter.is_katakana('アイ・エム・アイ'), False)

    def test_basic_filter(self):
        f = filter.WikipediaFilter()
        self.assertEqual(f.basic_filter('がちりん&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;'), 'がちりん')
        self.assertEqual(f.basic_filter('がちりん、がちがち'), 'がちりん')
        self.assertEqual(f.basic_filter('I&amp;O'), 'I&O')
        self.assertEqual(f.basic_filter('&amp;epsilon;-&amp;delta;論法'), 'ε-δ論法')
        self.assertEqual(f.basic_filter('I&amp;#9829;OGI'), 'I♥OGI')
        self.assertEqual(f.basic_filter('赤&#x2123D;眞弓'), '赤𡈽眞弓')
        self.assertEqual(f.basic_filter('山田 太郎'), '山田太郎')
        self.assertEqual(f.basic_filter('阿坂城跡附 高城跡枳城跡'), '阿坂城跡附高城跡枳城跡')
        self.assertEqual(f.basic_filter('足利 右兵衛督 成氏'), '足利右兵衛督成氏')

    def test_hojin_filter(self):
        f = filter.WikipediaFilter()
        # 株式会社少年画報社:しょうねんがほうしゃ -> 少年画報社:しょうねんがほうしゃ
        # 京浜急行電鉄株式会社:けいひんきゅうこうでんてつ -> 京浜急行電鉄:けいひんきゅうこうでんてつ
        self.assertEqual([f.hojin_filter('株式会社少年画報社', 'しょうねんがほうしゃ')], [('少年画報社', 'しょうねんがほうしゃ')])

    def test_validate_phase1(self):
        f = filter.WikipediaFilter()

        self.assertEqual(f.validate_phase1('又八郎', 'またはちろう'), True)
        self.assertEqual(f.validate_phase1('アクメスジト', 'またはあくめちぇっと'), False)
        self.assertEqual(f.validate_phase1('マタハリ百貨店', 'またはりひゃっかてん'), True)
        self.assertEqual(f.validate_phase1('イルーニャ', 'または'), False)

    def test_validate_phase2(self):
        f = filter.WikipediaFilter()

        self.assertEqual(f.validate_phase2('山田タロウ', 'やまだたろう'), True)

        self.assertEqual(f.validate_phase2('w3m', 'ダブリューサンエム または ダブリュースリーエム'), False)
        self.assertEqual(f.validate_phase2('3月', 'さんがつ'), False)
        self.assertEqual(f.validate_phase2('4004', 'よんまるまるよん'), False)
        self.assertEqual(f.validate_phase2('Keyboard / kAoru ikArAshi / 五十嵐 馨', 'いがらしかおる'), False)
        self.assertEqual(f.validate_phase2('ARIAの登場人物', 'ありあのとうじょうじんぶつ'), False)
        self.assertEqual(f.validate_phase2('アークライズファンタジアの登場キャラクター', 'あーくらいずふぁんたじあのとうじょうきゃらくたー'), False)
        self.assertEqual(f.validate_phase2('ウルトラQの登場怪獣', 'うるとらきゅーのとうじょうかいじゅう'), False)
        self.assertEqual(f.validate_phase2('仮面ライダー555の登場仮面ライダー', 'かめんらいだーふぁいずのとうじょうきゃらくたー'), False)
        self.assertEqual(f.validate_phase2('10.『七変化狸御殿』', 'しちへんげ たぬきごてん'), False)
        self.assertEqual(f.validate_phase2('第43話 - 第45話', 'ものくろ'), False)
        self.assertEqual(f.validate_phase2('キノミヤ信仰', 'しんこう'), False)
        self.assertEqual(f.validate_phase2('アイコナール近似', 'あいこなーるきんじ'), True)
        self.assertEqual(f.validate_phase2('アイム・キンキ理容美容専門学校', 'あいむきんきりようびようせんもんがっこう'), True)

if __name__ == '__main__':
    unittest.main()

