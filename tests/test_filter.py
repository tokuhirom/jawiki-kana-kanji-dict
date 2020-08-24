import unittest
from jawiki import filter

class TestWikipediaFilter(unittest.TestCase):

    def test_is_hiragana(self):
        self.assertEqual(filter.is_hiragana('めもり'), True)
        self.assertEqual(filter.is_hiragana('メモリ'), False)
        self.assertEqual(filter.is_hiragana('あいのめもりー'), True)

    def test_basic_filter(self):
        f = filter.WikipediaFilter()
        self.assertEqual(f.basic_filter('がちりん&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;'), 'がちりん')
        self.assertEqual(f.basic_filter('がちりん、がちがち'), 'がちりん')
        self.assertEqual(f.basic_filter('I&amp;O'), 'I&O')
        self.assertEqual(f.basic_filter('&amp;epsilon;-&amp;delta;論法'), 'ε-δ論法')
        self.assertEqual(f.basic_filter('I&amp;#9829;OGI'), 'I♥OGI')
        self.assertEqual(f.basic_filter('赤&#x2123D;眞弓'), '赤𡈽眞弓')

    def test_hojin_filter(self):
        f = filter.WikipediaFilter()
        # 株式会社少年画報社:しょうねんがほうしゃ -> 少年画報社:しょうねんがほうしゃ
        # 京浜急行電鉄株式会社:けいひんきゅうこうでんてつ -> 京浜急行電鉄:けいひんきゅうこうでんてつ
        self.assertEqual([f.hojin_filter('株式会社少年画報社', 'しょうねんがほうしゃ')], [('少年画報社', 'しょうねんがほうしゃ')])

    def test_is_valid(self):
        f = filter.WikipediaFilter()

        self.assertEqual(f.is_valid('山田タロウ', 'やまだたろう'), True)

        self.assertEqual(f.is_valid('w3m', 'ダブリューサンエム または ダブリュースリーエム'), False)
        self.assertEqual(f.is_valid('3月', 'さんがつ'), False)
        self.assertEqual(f.is_valid('4004', 'よんまるまるよん'), False)
        self.assertEqual(f.is_valid('Keyboard / kAoru ikArAshi / 五十嵐 馨', 'いがらしかおる'), False)
        self.assertEqual(f.is_valid('ARIAの登場人物', 'ありあのとうじょうじんぶつ'), False)
        self.assertEqual(f.is_valid('アークライズファンタジアの登場キャラクター', 'あーくらいずふぁんたじあのとうじょうきゃらくたー'), False)
        self.assertEqual(f.is_valid('ウルトラQの登場怪獣', 'うるとらきゅーのとうじょうかいじゅう'), False)
        self.assertEqual(f.is_valid('仮面ライダー555の登場仮面ライダー', 'かめんらいだーふぁいずのとうじょうきゃらくたー'), False)
        self.assertEqual(f.is_valid('10.『七変化狸御殿』', 'しちへんげ たぬきごてん'), False)

if __name__ == '__main__':
    unittest.main()

