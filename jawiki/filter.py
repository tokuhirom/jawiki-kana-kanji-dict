import regex
import re
import jaconv
import html

HIRAGANA_PATTERN = regex.compile(r'^[\p{Hiragana}ー]+$')

def is_hiragana(s):
    if HIRAGANA_PATTERN.match(s):
        return True
    else:
        return False

INVALID_KANJI_PATTERNS = [
    re.compile(r'^\d+(月|世紀|年代)'),
    # TITLE<<Intel 4004>> KANJI<<4004>> YOMI<<よんまるまるよん>> 8
    re.compile(r'^[0-9]+$'),
    # TITLE<<四川省>> KANJI<<{{仮リンク|巴蜀(歴史)|zh|巴蜀|label=巴蜀}}>> YOMI<<はしょく>> 4
    re.compile(r'\{\{仮リンク'),
    # r/^日本の企業一覧/, # TITLE<<日本の企業一覧 (その他製品)>> KANJI<<日本の企業一覧(その他製造)>> YOMI<<にほんのきぎょういちらんそのたせいぞう>> 19
    re.compile(r'^日本の企業一覧'),
    #   qr/の登場人物$/, # TITLE<<ときめきメモリアル2の登場人物>> KANJI<<ときめきメモリアル2の登場人物>> YOMI<<ときめきめもりあるつーのとうじょうじんぶつ>> 21
    re.compile(r'.*の登場(?:人物|キャラクター|仮面ライダー|怪獣|メカ|兵器|組織|馬|人物一覧|レスラー|人物の索引)$'),
]

HOJIN_PATTERNS = [
    ('株式会社', 'かぶしきがいしゃ'),
    ('有限会社', 'ゆうげんがいしゃ'),
    ('一般社団法人', 'いっぱんしゃだんほうじん'),
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

                if kanji.startswith('[['):
                    self.log_skip('kanji is page link', [kanji, yomi])
                    continue

                if yomi.startswith('[['):
                    self.log_skip('yomi is page link', [kanji, yomi])
                    continue

                kanji = self.basic_filter(kanji)
                yomi = self.basic_filter(yomi)
                yomi = jaconv.kata2hira(yomi)
                kanji, yomi = self.hojin_filter(kanji, yomi)

                if not self.is_valid(kanji, yomi):
                    continue

                yield (kanji, yomi)

    def is_valid(self, kanji, yomi):
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

        for kanji_prefix in ['〜', '『', '「', '〈','《']:
            if kanji.startswith(kanji_prefix):
                self.log_skip('kanji starts with %s' % kanji_prefix, [kanji, yomi])
                return False

        for yomi_prefix in [
            # '''[[マイクロソフト]]'''（ただし、[[Xbox 360]]はどちらの規格にも対応せず、[[Microsoft Windows Vista]]は両規格に対応していた）
            'ただし、'
            # この音は'''ハーフ・ストップ'''（あるいはエコー、ハーフ・ミュート）と呼ばれる。
            'あるいは']:
            if yomi.startswith(yomi_prefix):
                self.log_skip('yomi starts with %s' % yomi_prefix, [kanji, yomi])
                return False

        # yomi infx
        for infix in [
                # ''w3m'''（ダブリューサンエム または ダブリュースリーエム）
                ' または ',
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
            ]:
            if infix in kanji:
                self.log_skip('kanji contains %s' % infix, [kanji, yomi])
                return False

        for pattern in INVALID_KANJI_PATTERNS:
            if pattern.match(kanji):
                self.log_skip('Invalid kanji pattern', [kanji, yomi])
                return False


        return True

    def basic_filter(self, token):
        # &lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;
        token = re.sub(r'&lt;ref.*', '', token)

        token = re.sub(r'\{\{[Ll]ang-[a-z]+(?:-short)?\|.+?\}\}', '', token)

        # <!-- foobar -->
        token = re.sub(r'&lt;!--.*--&gt;', '', token)

        # {{lang|en|AMBAC}}
        token = re.sub(r'\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}', r'\1', token)

        # {{CP932フォント|髙}}千代酒造
        # '''司馬 {{JIS2004フォント|遼󠄁}}太郎'''
        # つじかおり /{{JIS90フォント|辻}}香緒里/
        # {{Anchor|穴子包丁}}
        # うじょう /{{Vanchor|羽状}}/
        # まっちでーじぇいりーぐ /マッチデー{{unicode|♥}}Jリーグ/
        # '''{{linktext|六根}}'''（ろっこん）
        token = re.sub(r'\{\{(?:En|IPA-en|要出典範囲|linktext|unicode|Anchor|Vanchor|[A-Z0-9]+フォント)\|(.+)\}\}', r'\1', token)

        # [[ページ名|リンクラベル]] 
        token = re.sub(r'\[\[(?:.*)\|(.*)\]\]', r'\1', token)

        # '''[[葉状体]]'''（ようじょうたい）
        # '''[[瘀血]]証'''（おけつしょう）
        token = re.sub(r'\[\[(.*)\]\]', r'\1', token)


        # '''池の平スノーパーク（旧白樺リゾートスキー場）'''（いけのたいらすのーぱーく）
        token = re.sub(r'（旧.*）', r'', token)

        token = re.sub(r'、.*', r'', token)

        token = re.sub(r'\s', r'', token)

        token = re.sub(r'&amp;', r'&', token)
        token = re.sub(r'(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)', lambda x: html.unescape(x[1]), token)

        return token

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
                kanji = kanji.rstrip(k)
            if kanji.endswith(k) and yomi.endswith(y):
                kanji = kanji.rstrip(k)
                yomi = yomi.rstrip(y)
        return (kanji, yomi)

