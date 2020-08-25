import re
import jaconv
import html

# TODO move following Japanese character related things to jawiki.chars

# https://note.nkmk.me/python-re-regex-character-type/
HIRAGANA_BLOCK = r'\u3041-\u309Fー'

# https://www.ncbi.nlm.nih.gov/staff/beck/charents/unicode/30A0-30FF.html
# 30FB  ・ は除外。
KATAKANA_BLOCK = r'\u30A1-\u30FA\u30FC-\u30FFー'

KANJI_BLOCK = r'\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u21000-\u213FF\U00020000-\U0002EBEF'

HIRAGANA_PATTERN = re.compile(r'^[' + HIRAGANA_BLOCK + ']+$')
KATAKANA_PATTERN = re.compile(r'^[' + KATAKANA_BLOCK + ']+$')
KANJI_PATTERN = re.compile(r'^[' + KANJI_BLOCK + ']+$')

NAMEISH_PATTERN = re.compile(r'([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)\s+([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)')

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
        yomi = self.basic_filter(yomi)
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

        for kanji_prefix in ['〜', '『', '「', '〈','《', '／']:
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
        # '''砂川奈美(旧姓:伊藤)'''（いさがわなみ、[[1991年]][[1月23日]] - ）
        token = re.sub(r'（旧.*?）', r'', token)
        token = re.sub(r'[（\(]旧姓:.*?[）\)]', r'', token)
        token = re.sub(r'（(\d+|[一-九])代目?）', r'', token)
        token = re.sub(r'（初代）', r'', token)

        token = re.sub(r'、.*', r'', token)

        # 先頭/末尾の中黒はマークアップ失敗なので、カバーしてあげる
        token = re.sub(r'^・', r'', token)
        token = re.sub(r'・$', r'', token)

        token = re.sub(r'&amp;', r'&', token)
        token = re.sub(r'(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)', lambda x: html.unescape(x[1]), token)

        # '山田 太朗' → 山田太朗
        while True:
            token, number_of_subs_made = re.subn(NAMEISH_PATTERN, r'\1\2', token)
            if number_of_subs_made==0:
                break

        return token.strip()

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

