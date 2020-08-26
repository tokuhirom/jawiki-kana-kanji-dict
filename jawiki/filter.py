import re
import jaconv
import html

# TODO move following Japanese character related things to jawiki.chars

# https://note.nkmk.me/python-re-regex-character-type/
HIRAGANA_BLOCK = r'\u3041-\u309Fー'

# https://www.ncbi.nlm.nih.gov/staff/beck/charents/unicode/30A0-30FF.html
# 30FB  ・ は除外。
KATAKANA_BLOCK = r'\u30A1-\u30FA\u30FC-\u30FFー'

KANJI_BLOCK = r'\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF'
# KANJI_BLOCK = r'\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u21000-\u213FF\U00020000-\U0002EBEF'

HIRAGANA_PATTERN = re.compile(r'^[' + HIRAGANA_BLOCK + ']+$')
KATAKANA_PATTERN = re.compile(r'^[' + KATAKANA_BLOCK + ']+$')
KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN = re.compile(r'^[ 　' + KATAKANA_BLOCK + HIRAGANA_BLOCK + '・]+$')
KANJI_PATTERN = re.compile(r'^[' + KANJI_BLOCK + ']+$')

NAMEISH_PATTERN = re.compile(r'([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)[\u0020\u3000]+([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)')

KANJI_NORMALIZER = str.maketrans('亞惡壓圍爲醫壹稻飮隱營榮衞驛悅閱圓緣艷鹽奧應橫歐毆黃溫穩假價畫會囘壞懷繪槪擴殼覺學嶽樂渴鐮勸卷寬歡罐觀閒關陷巖顏歸氣龜僞戲犧卻糺舊據擧虛峽挾敎强狹鄕堯曉區驅勳薰羣徑惠揭攜溪經繼莖螢輕鷄藝擊缺儉劍圈檢權獻縣硏險顯驗嚴吳娛效廣恆鑛號國黑歲濟碎齋劑冱櫻册雜產參慘棧蠶贊殘絲姊齒兒辭濕實舍寫釋壽收從澁獸縱肅處緖敍尙奬將牀涉燒稱證乘剩壤孃條淨狀疊穰讓釀囑觸寢愼晉眞刄盡圖粹醉隨髓數樞瀨淸靑聲靜齊稅蹟說攝竊絕專戰淺潛纖踐錢禪曾瘦雙遲壯搜插巢爭窗總聰莊裝騷增臟藏卽屬續墮體對帶滯臺瀧擇澤單擔膽團彈斷癡晝蟲鑄廳徵聽敕鎭脫遞鐵轉點傳黨盜燈當鬭德獨讀屆繩貳姙黏惱腦霸廢拜賣麥發髮拔晚蠻祕彥姬濱甁拂佛倂竝變邊辨瓣辯舖步穗寶萠襃豐沒飜槇每萬滿麵默餠歷戀戾彌藥譯豫餘與譽搖樣謠遙瑤慾來賴亂覽畧龍兩獵綠鄰凜壘淚勵禮隸靈齡曆鍊爐勞樓郞祿錄亙灣', '亜悪圧囲為医壱稲飲隠営栄衛駅悦閲円縁艶塩奥応横欧殴黄温穏仮価画会回壊懐絵概拡殻覚学岳楽渇鎌勧巻寛歓缶観間関陥巌顔帰気亀偽戯犠却糾旧拠挙虚峡挟教強狭郷尭暁区駆勲薫群径恵掲携渓経継茎蛍軽鶏芸撃欠倹剣圏検権献県研険顕験厳呉娯効広恒鉱号国黒歳済砕斎剤冴桜冊雑産参惨桟蚕賛残糸姉歯児辞湿実舎写釈寿収従渋獣縦粛処緒叙尚奨将床渉焼称証乗剰壌嬢条浄状畳穣譲醸嘱触寝慎晋真刃尽図粋酔随髄数枢瀬清青声静斉税跡説摂窃絶専戦浅潜繊践銭禅曽双痩遅壮捜挿巣争窓総聡荘装騒増臓蔵即属続堕体対帯滞台滝択沢単担胆団弾断痴昼虫鋳庁徴聴勅鎮脱逓鉄転点伝党盗灯当闘徳独読届縄弐妊粘悩脳覇廃拝売麦発髪抜晩蛮秘彦姫浜瓶払仏併並変辺弁弁弁舗歩穂宝萌褒豊没翻槙毎万満麺黙餅歴恋戻弥薬訳予余与誉揺様謡遥瑶欲来頼乱覧略竜両猟緑隣凛塁涙励礼隷霊齢暦錬炉労楼郎禄録亘湾')

def kanji_normalize(s):
    return s.translate(KANJI_NORMALIZER)

def is_katakana_or_hiragana_or_nakaguro_or_space(s):
    if KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN.match(s):
        return True
    else:
        return False

def is_hiragana(s):
    if HIRAGANA_PATTERN.match(s):
        return True
    else:
        return False

def is_katakana(s):
    if KATAKANA_PATTERN.match(s):
        return True
    else:
        return False

def is_kanji(s):
    if KANJI_PATTERN.match(s):
        return True
    else:
        return False

INVALID_KANJI_PATTERNS = [
    re.compile(r'^\d+(月|世紀|年代)'),
    # TITLE<<Intel 4004>> KANJI<<4004>> YOMI<<よんまるまるよん>> 8
    re.compile(r'^[0-9]+$'),
    # '''10.『七変化狸御殿』'''（しちへんげ たぬきごてん）
    re.compile(r'^[0-9]+\.『'),
    # TITLE<<四川省>> KANJI<<{{仮リンク|巴蜀(歴史)|zh|巴蜀|label=巴蜀}}>> YOMI<<はしょく>> 4
    re.compile(r'\{\{仮リンク'),
    # r/^日本の企業一覧/, # TITLE<<日本の企業一覧 (その他製品)>> KANJI<<日本の企業一覧(その他製造)>> YOMI<<にほんのきぎょういちらんそのたせいぞう>> 19
    re.compile(r'^日本の企業一覧'),
    #   qr/の登場人物$/, # TITLE<<ときめきメモリアル2の登場人物>> KANJI<<ときめきメモリアル2の登場人物>> YOMI<<ときめきめもりあるつーのとうじょうじんぶつ>> 21
    re.compile(r'.*の登場(?:人物|キャラクター|仮面ライダー|怪獣|メカ|兵器|組織|馬|人物一覧|レスラー|人物の索引)$'),
    # '第43話 - 第45話', 'ものくろ'
    re.compile(r'第\d+話'),
]

HOJIN_PATTERNS = [
    ('株式会社', 'かぶしきがいしゃ'),
    ('合同会社', 'ごうどうがいしゃ'),
    ('有限会社', 'ゆうげんがいしゃ'),
    ('一般社団法人', 'いっぱんしゃだんほうじん'),
    ('一般財団法人', 'いっぱんざいだんほうじん'),
    ('学校法人', 'がっこうほうじん'),
    ('公益財団法人', 'こうえきざいだんほうじん'),
    ('公益社団法人','こうえきしゃだんほうじん'),
    ('特定非営利活動法人','とくていひえいりかつどうほうじん'),
]

def default_skip_logger(reason, line):
    print("<<<%s>>> %s" % (reason, line))

class WikipediaFilter:

    def __init__(self, skip_logger = default_skip_logger):
        self.skip_logger = skip_logger

    def log_skip(self, reason, line):
        self.skip_logger(reason, line)
        # print("<<<%s>>> %s" % (reason, line))

    def filter(self, srcfname):
        with open(srcfname, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                splitted = line.split("\t")
                if len(splitted) != 3:
                    continue

                (title, kanji, yomi) = splitted

                m = self.filter_entry(title, kanji, yomi)
                if m:
                    kanji, yomi = m
                    yield (kanji, yomi)

    def filter_entry(self, title, kanji, yomi):
        if kanji.startswith('[['):
            self.log_skip('kanji is page link', [kanji, yomi])
            return

        if not self.validate_phase1(title, kanji, yomi):
            return

        kanji = self.basic_filter(kanji)
        kanji = self.kanji_filter(kanji)
        yomi = self.basic_filter(yomi)
        yomi = self.yomi_filter(yomi, kanji)
        yomi = jaconv.kata2hira(yomi)
        kanji, yomi = self.hojin_filter(kanji, yomi)

        # remove spaces in yomi
        yomi = re.sub(r'\s', r'', yomi)
        # 全角スペースを半角に
        kanji = re.sub(r'\s', r' ', kanji)

        if not self.validate_phase2(kanji, yomi):
            return

        return (kanji, yomi)

    def validate_phase1(self, title, kanji, yomi):
        for yomi_prefix in ['[[', 'いま、', 'あるいは', 'もしくは']:
            if yomi.startswith(yomi_prefix):
                self.log_skip('ignorable yomi prefix: %s' % (yomi_prefix), [kanji, yomi])
                return False

        for kanji_prefix in ['』']:
            if kanji.startswith(kanji_prefix):
                self.log_skip('ignorable kanji prefix: %s' % (kanji_prefix), [kanji, yomi])
                return False

        # 「または」で始まるものは基本的に除外したほうがいいが、いくつかだけキャッチアップしよう。
        if yomi.startswith('または'):
            if len([1 for n in ['またはちろう', 'またはりひゃっかてん', 'またはり'] if yomi.startswith(n)])==0:
                self.log_skip('ignorable yomi prefix: %s' % (yomi_prefix), [kanji, yomi])
                return False

        if title in [
            # カッコ内に元になったマイクロンが入っているので無視。
            'トランスフォーマー ギャラクシーフォース',
            # 読み仮名が中途半端に入っている。古いアプリの情報なので一次情報をたどるのが難しくwikipedia川を修正するのが困難なので無視。
            'アイドル・ジェネレーション 第2次・萌えっ子大戦争!!',
            # ライトノベル独自用語
            'Dクラッカーズ',
        ]:
            self.log_skip('Title is in the blacklist', [title, kanji, yomi])
            return False

        return True

    def validate_phase2(self, kanji, yomi):
        if len(kanji) == 0:
            self.log_skip('kanji is empty', [kanji, yomi])
            return False

        if len(kanji) == 1:
            self.log_skip('kanji is single character', [kanji, yomi])
            return False

        if len(yomi) == 0:
            self.log_skip('yomi is empty', [kanji, yomi])
            return False

        if len(yomi) < 2:
            self.log_skip('yomi is too short', [kanji, yomi])
            return False

        if not is_hiragana(yomi):
            self.log_skip('yomi contains non-hiragana char', [kanji, yomi])
            return False

        if is_hiragana(kanji):
            self.log_skip('kanji is hiragana', [kanji, yomi])
            return False

        for kanji_prefix in ['〜', '『', '「', '＜', '〈','《', '／', '日本の']:
            if kanji.startswith(kanji_prefix):
                self.log_skip('kanji starts with %s' % kanji_prefix, [kanji, yomi])
                return False

        for kanji_postfix in ['・']:
            if kanji.endswith(kanji_postfix):
                self.log_skip('kanji ends with %s' % kanji_postfix, [kanji, yomi])
                return False

        for yomi_prefix in [
            # '''[[マイクロソフト]]'''（ただし、[[Xbox 360]]はどちらの規格にも対応せず、[[Microsoft Windows Vista]]は両規格に対応していた）
            'ただし、',
            # この音は'''ハーフ・ストップ'''（あるいはエコー、ハーフ・ミュート）と呼ばれる。
            'あるいは',
            'おりんぴっくの',]:
            if yomi.startswith(yomi_prefix):
                self.log_skip('yomi starts with %s' % yomi_prefix, [kanji, yomi])
                return False

        # yomi infx
        for infix in [
                # ''w3m'''（ダブリューサンエム または ダブリュースリーエム）
                ' または ',
                'における',
                "'''",
                '[',
            ]:
            if infix in yomi:
                self.log_skip('yomi contains %s' % infix, [kanji, yomi])
                return False

        # kanji infx
        for infix in [
                # '''Keyboard / kAoru ikArAshi / 五十嵐 馨'''（いからし かおる）
                '/',
                "''",
                '{{',
                '[[',
                '(',
                '（',
            ]:
            if infix in kanji:
                self.log_skip('kanji contains %s' % infix, [kanji, yomi])
                return False

        for pattern in INVALID_KANJI_PATTERNS:
            if pattern.match(kanji):
                self.log_skip('Invalid kanji pattern', [kanji, yomi])
                return False

        m = re.match(r'^([' + KATAKANA_BLOCK + ']+)', kanji)
        if m:
            prefix = m[1]
            prefix_hira = jaconv.kata2hira(prefix)
            if not (yomi.startswith(prefix_hira) or yomi.startswith(prefix_hira.replace('ゐ', 'い'))):
                self.log_skip("Kanji prefix and yomi prefix aren't same: " + prefix, [kanji, yomi])
                return False

        return True

    def basic_filter(self, token):
        # &lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;
        token = re.sub(r'&lt;ref.*', '', token)

        # token = re.sub(r'\{\{[Ll]ang-[a-z]+(?:-short)?\|.+?\}\}', '', token)

        # <!-- foobar -->
        token = re.sub(r'&lt;!--.*--&gt;', '', token)

        # '''[[葉状体]]'''（ようじょうたい）
        # '''[[瘀血]]証'''（おけつしょう）
        # token = re.sub(r'\[\[(.*)\]\]', r'\1', token)

        # '''池の平スノーパーク（旧白樺リゾートスキー場）'''（いけのたいらすのーぱーく）
        # '''砂川奈美(旧姓:伊藤)'''（いさがわなみ、[[1991年]][[1月23日]] - ）
        token = re.sub(r'（旧.*?）', r'', token)
        token = re.sub(r'[（\(](旧姓|本名)[:：].*?[）\)]', r'', token)
        token = re.sub(r'（(\d+|[一-九])代目?）', r'', token)
        token = re.sub(r'（初代）', r'', token)

        # token = re.sub(r'、.*', r'', token)

        # 先頭/末尾の中黒はマークアップ失敗なので、カバーしてあげる
        token = re.sub(r'^・', r'', token)
        token = re.sub(r'・$', r'', token)

        token = re.sub(r'&amp;', r'&', token)
        token = re.sub(r'(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)', lambda x: html.unescape(x[1]), token)

        return token.strip()

    def kanji_filter(self, kanji):
        # {{lang|en|AMBAC}}
        kanji = re.sub(r'\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}', r'\1', kanji)

        # {{CP932フォント|髙}}千代酒造
        # '''司馬 {{JIS2004フォント|遼󠄁}}太郎'''
        # つじかおり /{{JIS90フォント|辻}}香緒里/
        # {{Anchor|穴子包丁}}
        # うじょう /{{Vanchor|羽状}}/
        # まっちでーじぇいりーぐ /マッチデー{{unicode|♥}}Jリーグ/
        # '''{{linktext|六根}}'''（ろっこん）
        kanji = re.sub(r'\{\{(?:En|IPA-en|要出典範囲|linktext|unicode|Anchor|Vanchor|[A-Z0-9]+フォント)\|(.+)\}\}', r'\1', kanji)

        # [[ページ名|リンクラベル]] 
        kanji = re.sub(r'\[\[(?:.*)\|(.*)\]\]', r'\1', kanji)
        kanji = re.sub(r'\[\[(.*)\]\]', r'\1', kanji)

        # '山田 太朗' → 山田太朗
        while True:
            kanji, number_of_subs_made = re.subn(NAMEISH_PATTERN, r'\1\2', kanji)
            if number_of_subs_made==0:
                break

        return kanji

    def yomi_filter(self, yomi, kanji=''):
        # [[慶應]]3年
        # yomi = re.sub(r"\[\[[" + KANJI_BLOCK + "]+\]\]\d+年.*", '', yomi)
        pyomi = yomi
        while True:
            yomi = re.sub(r'、声 - .*', '', yomi)
            yomi = re.sub(r'\[\[\d+年\]\].*', '', yomi)
            yomi = re.sub(r'\[\[\d+月\d+日\]\].*', '', yomi)
            yomi = re.sub(r"''.*", '', yomi)
            yomi = re.sub(r"\{\{.*", '', yomi)
            yomi = re.sub(r'\d+月\d+日.*', '', yomi)
            yomi = re.sub(r'\?\s*-\s*$', '', yomi)
            yomi = re.sub(r'[、][a-zA-Z]+[' + KANJI_BLOCK + ']+$', '', yomi)
            yomi = re.sub(r'[、][' + KANJI_BLOCK + ']+$', '', yomi)
            yomi = re.sub(r'[、][「].*', '', yomi)
            yomi = re.sub(r'(?:[' + KANJI_BLOCK + ']+)?([0-9?]+|元)年.*', '', yomi)
            yomi = re.sub(r'(生年不詳|生年月日非公表|生没年不詳).*', '', yomi)
            yomi = re.sub(r'現在の芸名.*', '', yomi)
            yomi = re.sub(r'\[\[[' + KANJI_BLOCK + ']+]].*', '', yomi)
            yomi = re.sub(r'(?:現姓|旧姓|通称|英文名|原題|ドイツ語|英語|英語表記|英語名称|英文社名|オランダ語|満州語|旧|旧芸名|中国語簡体字|漢語名字|略称|本名|英称|英)[:：は・].*', '', yomi)
            yomi = re.sub(r'[（:：,]\s*$', '', yomi)
            yomi = re.sub(r'[,、][（:：,]\s*$', '', yomi)
            yomi = re.sub(r'[,、]\[\[.*$', '', yomi)
            yomi = re.sub(r'''[、,][ A-Za-z.'&]+$''', '', yomi)
            yomi = re.sub(r'''[、,][ A-Za-z.'-''' + KANJI_BLOCK + ''']+$''', '', yomi)
            yomi = re.sub(r'、[（:：\-]*[ A-Za-z]+$', '', yomi)
            yomi = re.sub(r'、(詳しくは|本名同じ).*$', '', yomi)
            yomi = re.sub(r'[？?、－]+\s*$', '', yomi)
            yomi = re.sub(r'\s*$', '', yomi)
            yomi = re.sub(r'\[\[$', '', yomi)

            if pyomi == yomi:
                break
            else:
                pyomi = yomi

        # アイエスオー、イソ、アイソ to アイエスオー
        if all([is_katakana_or_hiragana_or_nakaguro_or_space(s) for s in yomi.split('、')]):
            yomi = yomi.split('、')[0]

        # 'やまだ たろう' → 'やまだたろう'
        while True:
            yomi, number_of_subs_made = re.subn(NAMEISH_PATTERN, r'\1\2', yomi)
            if number_of_subs_made==0:
                break

        if '、' in yomi:
            yomi = "、".join([s for s in yomi.split('、') if kanji != kanji_normalize(s)])

        return yomi

    # 株式会社少年画報社:しょうねんがほうしゃ -> 少年画報社:しょうねんがほうしゃ
    # 京浜急行電鉄株式会社:けいひんきゅうこうでんてつ -> 京浜急行電鉄:けいひんきゅうこうでんてつ
    def hojin_filter(self, kanji, yomi):
        for f in HOJIN_PATTERNS:
            (k, y) = f
            if kanji.startswith(k) and not yomi.startswith(y):
                kanji = kanji.lstrip(k)
            if kanji.startswith(k) and yomi.startswith(y):
                kanji = kanji.lstrip(k)
                yomi = yomi.lstrip(y)
            if kanji.endswith(k) and not yomi.endswith(y):
                kanji = kanji[:-len(k)]
            if kanji.endswith(k) and yomi.endswith(y):
                kanji = kanji[:-len(k)]
                yomi = yomi[:-len(y)]
        return (kanji, yomi)

