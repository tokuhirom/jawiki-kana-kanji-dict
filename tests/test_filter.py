import unittest
from jawiki import filter

class TestWikipediaFilter(unittest.TestCase):

    def test_is_kanji(self):
        self.assertEqual(filter.is_kanji('KEIYOGINKO'), False)
        self.assertEqual(filter.is_kanji('粟飯原首胤度'), True)

    def test_is_hiragana(self):
        self.assertEqual(filter.is_hiragana('めもり'), True)
        self.assertEqual(filter.is_hiragana('メモリ'), False)
        self.assertEqual(filter.is_hiragana('あいのめもりー'), True)
        self.assertEqual(filter.is_hiragana('KEIYOGINKO'), False)

    def test_is_katakana(self):
        self.assertEqual(filter.is_katakana('メモリ'), True)
        self.assertEqual(filter.is_katakana('アイ・エム・アイ'), False)
        self.assertEqual(filter.is_katakana('KEIYOGINKO'), False)

    def test_basic_filter(self):
        f = filter.WikipediaFilter()
        self.assertEqual(f.basic_filter('KEIYOGINKO POWER COUNTDOWN REAL'), 'KEIYOGINKO POWER COUNTDOWN REAL')
        self.assertEqual(f.basic_filter('がちりん&lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;'), 'がちりん')
        # self.assertEqual(f.basic_filter('がちりん、がちがち'), 'がちりん')
        self.assertEqual(f.basic_filter('I&amp;O'), 'I&O')
        self.assertEqual(f.basic_filter('&amp;epsilon;-&amp;delta;論法'), 'ε-δ論法')
        self.assertEqual(f.basic_filter('I&amp;#9829;OGI'), 'I♥OGI')
        self.assertEqual(f.basic_filter('赤&#x2123D;眞弓'), '赤𡈽眞弓')
        self.assertEqual(f.basic_filter('阿坂城跡附 高城跡枳城跡'), '阿坂城跡附高城跡枳城跡')
        self.assertEqual(f.basic_filter('足利 右兵衛督 成氏'), '足利右兵衛督成氏')
        self.assertEqual(f.basic_filter('砂川奈美(旧姓:伊藤)'), '砂川奈美')
        self.assertEqual(f.basic_filter('篠宮慶子（本名：篠宮景子）'), '篠宮慶子')

    def test_basic_filter(self):
        f = filter.WikipediaFilter()
        self.assertEqual(f.kanji_filter('山田 太郎'), '山田太郎')

    def test_hojin_filter(self):
        f = filter.WikipediaFilter()
        # 株式会社少年画報社:しょうねんがほうしゃ -> 少年画報社:しょうねんがほうしゃ
        # 京浜急行電鉄株式会社:けいひんきゅうこうでんてつ -> 京浜急行電鉄:けいひんきゅうこうでんてつ
        self.assertEqual([f.hojin_filter('株式会社少年画報社', 'しょうねんがほうしゃ')], [('少年画報社', 'しょうねんがほうしゃ')])

    def test_filter_entry(self):
        f = filter.WikipediaFilter()
        # self.assertEqual([f.filter_entry('a', 'KEIYOGINKO POWER COUNTDOWN REAL', """けいようぎんこう パワー・カウントダウン・リアル。略称&quot;'''パワカン'''&quot;""")], [('KEIYOGINKO POWER COUNTDOWN REAL', 'けいようぎんこうぱわーかうんとだうんりある')])
        self.assertEqual(
            [f.filter_entry('a', 'あぁ〜しらき', """ああしらき、[[1976年]][[11月21日]] - """)],
            [('あぁ〜しらき', 'ああしらき')])
        self.assertEqual(
            [f.filter_entry('a', '荒木理恵', """ああき りえ、1983年3月12日 - """)],
            [('荒木理恵', 'ああきりえ')])
        self.assertEqual(
            [f.filter_entry('a', 'アイアム野田', """あいあむのだ、本名:'''野田 祐介'''（のだ ゆうすけ""")],
            [('アイアム野田', 'あいあむのだ')])
        self.assertEqual(
            [f.filter_entry('a', 'アイアン郡', """あいあんぐん、 Iron County""")],
            [('アイアン郡', 'あいあんぐん')])
        self.assertEqual(
            [f.filter_entry('a', 'IRON-CHINO', """アイアンチノ、[[5月28日]] -""")],
            [('IRON-CHINO', 'あいあんちの')])
        self.assertEqual(
            [f.filter_entry('a', 'IAMエージェンシー', """アイアムエージェンシー、''IAM Agency''""")],
            [('IAMエージェンシー', 'あいあむえーじぇんしー')])
        self.assertEqual(
            [f.filter_entry('a', '愛育幼稚園', """あいいくようちえん、{{Llang|en|言語記事名=英語|Aiiku Kindergarten}}""")],
            [('愛育幼稚園', 'あいいくようちえん')])
        self.assertEqual(
            [f.filter_entry('a', 'ISO', """アイエスオー、イソ、アイソ""")],
            [('ISO', 'あいえすおー')])
        self.assertEqual(
            [f.filter_entry('a', 'ISV', """アイエスヴィ、{{lang-en|independent software vendor}} の略""")],
            [('ISV', 'あいえすゔぃ')])
        self.assertEqual(
            [f.filter_entry('a', '愛新覚羅溥傑', """あいしんかくら ふけつ、アイシンギョロ・プギェ、{{lang-mnc|ᠠᡞᠰᡞᠨ ᡤᡞᠣᠷᠣ&lt;br&gt;ᡦᡠ ᡤᡞᠶᡝ}}　転写：aisin-gioro pu-giye、[[1907年]][[4月16日]] - [[1994年]][[2月28日]]""")],
            [('愛新覚羅溥傑', 'あいしんかくらふけつ')])
        self.assertEqual(
                [f.filter_entry('a', '相生森林美術館', """あいおいしんりんびじゅつかん、[[英語|英称]]:''Aioi Shinrin Museum of Art''""")],
            [('相生森林美術館', 'あいおいしんりんびじゅつかん')])
        self.assertEqual(
                [f.filter_entry('a', '相生 由太郎', """あいおい よしたろう、[[慶応]]3年[[4月28日 (旧暦)|4月28日]]（[[1867年]][[5月31日]]""")],
            [('相生由太郎', 'あいおいよしたろう')])
        self.assertEqual(
                [f.filter_entry('a', 'アイオワ郡', """あいおわぐん、: Iowa County""")],
            [('アイオワ郡', 'あいおわぐん')])
        self.assertEqual(
                [f.filter_entry('a', 'アイオン台風', """アイオンたいふう、昭和23年台風第21号、国際名：'''アイオン'''/''Ione''""")],
            [('アイオン台風', 'あいおんたいふう')])
        self.assertEqual(
                [f.filter_entry('a', 'アイカテック建材株式会社', """アイカテックけんざい、[[英語|英文]]社名 ''Aica Tech Kenzai Corporation''""")],
            [('アイカテック建材', 'あいかてっくけんざい')])
        self.assertEqual(
                [f.filter_entry('a', 'アイオー信用金庫', """アイオーしんようきんこ、[[英語]]：''I･O Shinkin Bank''""")],
            [('アイオー信用金庫', 'あいおーしんようきんこ')])
        self.assertEqual(
                [f.filter_entry('a', 'アイルランド共産党', """アイルランドきょうさんとう、[[英語]]:'''The Communist Party of Ireland'''、[[アイルランド語]]:'''Páirtí Cumannach na hÉireann'''、略称'''CPI'''""")],
            [('アイルランド共産党', 'あいるらんどきょうさんとう')])
        self.assertEqual(
                [f.filter_entry('a', '哀川翔', """あいかわ しょう、（英:''Show Aikawa''""")],
            [('哀川翔', 'あいかわしょう')])
        self.assertEqual(
                [f.filter_entry('a', '哀 章', """あい しょう、? - [[23年]]""")],
            [('哀章', 'あいしょう')])
        self.assertEqual(
                [f.filter_entry('a', '愛新覚羅 胤礽', """あいしんかくら いんじょう、[[満州語]]：{{mongol|ᠠᡞᠰᡞᠨ ᡤᡞᠣᠷᠣ&lt;br&gt;ᡞᠨ ᠴᡝᠩ}}、転写：aisin-gioro in-ceng、[[1674年]]6月6日 - [[1725年]]1月20日""")],
            [('愛新覚羅胤礽', 'あいしんかくらいんじょう')])
        self.assertEqual(
                [f.filter_entry('a', 'アイオリス人', """アイオリスじん、Aioleis, {{lang-el|Αἰολεῖς}})""")],
            [('アイオリス人', 'あいおりすじん')])
        self.assertEqual(
                [f.filter_entry('a', 'IERS基準子午線', """アイイーアールエスきじゅんしごせん、IERS Reference Meridian, IRM""")],
            [('IERS基準子午線', 'あいいーあーるえすきじゅんしごせん')])
        self.assertEqual(
                [f.filter_entry('a', '安威 資脩', """あい すけなが、？－[[応安]]4年/[[建徳]]2年[[8月1日 (旧暦)|8月1日]]（[[1371年]][[9月10日]]""")],
            [('安威資脩', 'あいすけなが')])
        self.assertEqual(
                [f.filter_entry('a', '愛がいっぱい', """あい-""")],
            [None])
        self.assertEqual(
                [f.filter_entry('a', '』AIS『', """アイス : 淳の休日アイドルスクランブル atsushi's holiday idol scramble""")],
            [None])
        self.assertEqual(
                [f.filter_entry('a', 'IQVIAソリューションズ ジャパン株式会社', """アイキューヴィアソリューションズジャパン、IQVIA Solutions Japan K.K.""")],
            [('IQVIAソリューションズジャパン', 'あいきゅーゔぃあそりゅーしょんずじゃぱん')])
        self.assertEqual(
                [f.filter_entry('a', '愛国者の日', """あいこくしゃのひ、Patriots' Day""")],
            [('愛国者の日', 'あいこくしゃのひ')])
        self.assertEqual(
                [f.filter_entry('a', '逢坂 南', """あいさか みなみ、Minami Aisaka、[[1994年]][[10月26日]]&lt;ref name=&quot;profile&quot;&gt;{{cite news|url = http://casting.jp/model_talent/aisaka_minami/index.html| title =プロフィール|publisher =公式サイト}}&lt;/ref&gt; -""")],
            [('逢坂南', 'あいさかみなみ')])
        self.assertEqual(
                [f.filter_entry('a', '愛国戦線', """あいこくせんせん、Patriotic Front、略称：'''PF'''""")],
            [('愛国戦線', 'あいこくせんせん')])
        self.assertEqual(
                [f.filter_entry('a', 'あおやぎ 孝夫', """あおやぎ たかお、197?年[[12月13日]]&lt;ref name=&quot;sunday&quot;&gt;「[http://web.archive.org/web/20040609180941/http://www.websunday.net/backstage/aoyagi.html サンデー漫画家バックステージ　あおやぎ孝夫]」（[[インターネットアーカイブ]]のキャッシュ""")],
            [('あおやぎ孝夫', 'あおやぎたかお')])
        self.assertEqual(
                [f.filter_entry('a', '鮎沢 伊太夫', """あいざわ いだゆう、あゆさわ　いだゆう[[文政]]7年（[[1824年]]""")],
            [('鮎沢伊太夫', 'あいざわいだゆう')])
        self.assertEqual(
                [f.filter_entry('a', 'ISISちゃん', """アイシスちゃん、ISIS-chan&lt;ref name=thetimes4549102/&gt;&lt;ref name=moneycnnisis-chan&gt;{{Cite web||date=2015.07.23 |url=http://money.cnn.com/2015/07/23/technology/isis-chan/|author=Jose Pagliery|title=Anime nerds trying to Google bomb ISIS|work=[[:en:CNNMoney|CNNMoney]]|publisher=[[CNN]]|accessdate=2015-10-05|language=英語}}&lt;/ref&gt;&lt;ref name=fortunewyden-terrorism/&gt;&lt;ref name=dw18698611/&gt;&lt;ref name=albawaba724808/&gt;""")],
            [('ISISちゃん', 'あいしすちゃん')])
        self.assertEqual(
                [f.filter_entry('a', 'ri動詞', """アイスランド語:ri-sagnir""")],
            [None])
        self.assertEqual(
                [f.filter_entry('a', '相川 紗登士', """あいかわ さとし、生年月日非公表&lt;ref name=&quot;局アナnet&quot;&gt;{{Cite web |url=http://www.kyokuana.net/profile.html?id=146 |title=相川 紗登士 |website=JKN=局アナnet |publisher=JAT株式会社 |accessdate=2020-08-19}}&lt;/ref&gt;""")],
            [('相川紗登士', 'あいかわさとし')])
        self.assertEqual(
                [f.filter_entry('a', '愛玩動物看護師法', """あいがんどうぶつかんごしほう、令和元年6月28日法律第50号""")],
            [('愛玩動物看護師法', 'あいがんどうぶつかんごしほう')])
        self.assertEqual(
                [f.filter_entry('a', '愛国路駅', """あいこくろえき、中国語簡体字：爱国路站、英語：Aiguo Road Station""")],
            [('愛国路駅', 'あいこくろえき')])
        self.assertEqual(
                [f.filter_entry('a', '青木 優', """あおき ゆう、生没年不詳""")],
            [('青木優', 'あおきゆう')])
        self.assertEqual(
                [f.filter_entry('a', 'IOK-1銀河', """アイオーケーワンぎんが、英語：IOK-1 Galaxy""")],
            [('IOK-1銀河', 'あいおーけーわんぎんが')])
        self.assertEqual(
                [f.filter_entry('a', 'IQプロジェクト研究生', """あいきゅープロジェクトけんきゅうせい、IQP研究生""")],
            [('IQプロジェクト研究生', 'あいきゅーぷろじぇくとけんきゅうせい')])
        self.assertEqual(
                [f.filter_entry('a', '葛見やよい', """くずみ やよい、声 - [[相沢舞]]""")],
            [('葛見やよい', 'くずみやよい')])
        self.assertEqual(
                [f.filter_entry('a', '相沢 忠洋', """あいざわ ただひろ、相澤 忠洋、[[1926年]]（大正15年""")],
            [('相沢忠洋', 'あいざわただひろ')])
        self.assertEqual(
                [f.filter_entry('a', '愛新覚羅 鴻潤', """あいしんかくら こうじゅん、漢語名字：金 鴻潤""")],
            [('愛新覚羅鴻潤', 'あいしんかくらこうじゅん')])
        self.assertEqual(
                [f.filter_entry('a', '相田 楓', """あいだ かえで、現在の芸名は'''桜川 千夏'''（さくらがわ ちなつ""")],
            [('相田楓', 'あいだかえで')])
        self.assertEqual(
                [f.filter_entry('a', '愛情の花咲く樹', """あいじょうのはなさくき、原題：''Raintree County''""")],
            [('愛情の花咲く樹', 'あいじょうのはなさくき')])
        self.assertEqual(
                [f.filter_entry('a', '会田 安明', """あいだ やすあき、「やすあきら」とも、[[延享]]4年[[2月10日 (旧暦)|2月10日]]（[[1747年]][[3月20日]]""")],
            [('会田安明', 'あいだやすあき')])
        self.assertEqual(
                [f.filter_entry('a', '愛知県地方木材株式会社', """あいちけんちほうもくざいかぶしきがいしゃ、地木社""")],
            [('愛知県地方木材', 'あいちけんちほうもくざい')])

    def test_validate_phase1(self):
        f = filter.WikipediaFilter()

        self.assertEqual(f.validate_phase1('a', '又八郎', 'またはちろう'), True)
        self.assertEqual(f.validate_phase1('a', 'アクメスジト', 'またはあくめちぇっと'), False)
        self.assertEqual(f.validate_phase1('a', 'マタハリ百貨店', 'またはりひゃっかてん'), True)
        self.assertEqual(f.validate_phase1('a', 'イルーニャ', 'または'), False)

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

