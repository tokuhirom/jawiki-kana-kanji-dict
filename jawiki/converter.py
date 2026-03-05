import logging
import re

import jaconv

from jawiki.hojin import hojin_filter
from statistics import mean

import Levenshtein
import html

from jawiki.jachars import HIRAGANA_BLOCK, KANJI_BLOCK, KATAKANA_BLOCK, kanji_normalize

NAMEISH_PATTERN = re.compile(r"([" + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + "]+)" + "[\u0020\u3000]+([" + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + "]+)")

KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN = re.compile(r"^[ 　" + KATAKANA_BLOCK + HIRAGANA_BLOCK + "・]+$")

# basic_filter patterns
_RE_LT_REF = re.compile(r"&lt;ref.*")
_RE_COMMENT = re.compile(r"&lt;!--.*--&gt;")
_RE_KYUU = re.compile(r"（旧.*?）")
_RE_KYUUSEI = re.compile(r"[（\(](旧姓|本名)[:：].*?[）\)]")
_RE_DAIME = re.compile(r"（(\d+|[一-九])代目?）")
_RE_SHODAI = re.compile(r"（初代）")
_RE_LEADING_NAKAGURO = re.compile(r"^・")
_RE_TRAILING_NAKAGURO = re.compile(r"・$")
_RE_AMP = re.compile(r"&amp;")
_RE_HTML_ENTITY = re.compile(r"(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)")

# kanji_filter patterns
_RE_LANG = re.compile(r"\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}")
_RE_TEMPLATE = re.compile(r"\{\{(?:En|IPA-en|要出典範囲|linktext|unicode|Anchor|Vanchor|[A-Z0-9]+フォント)\|(.+)\}\}")
_RE_WIKILINK_LABEL = re.compile(r"\[\[(?:.*)\|(.*)\]\]")
_RE_WIKILINK = re.compile(r"\[\[(.*)\]\]")
_RE_WHITESPACE = re.compile(r"\s+")

# yomi_filter patterns
_RE_NOCHINO = re.compile(r"^のちの('''|\[\[).*")
_RE_VOICE = re.compile(r"、声 - .*")
_RE_YEAR_LINK = re.compile(r"\[\[\d+年\]\].*")
_RE_DATE_LINK = re.compile(r"\[\[\d+月\d+日\]\].*")
_RE_BOLD = re.compile(r"''.*")
_RE_TEMPLATE_OPEN = re.compile(r"\{\{.*")
_RE_DATE = re.compile(r"\d+月\d+日.*")
_RE_QUESTION_DASH = re.compile(r"\?\s*-\s*$")
_RE_COMMA_ALPHA_KANJI = re.compile(r"[、][a-zA-Z]+[" + KANJI_BLOCK + "]+$")
_RE_COMMA_KANJI = re.compile(r"[、][" + KANJI_BLOCK + "]+$")
_RE_COMMA_BRACKET = re.compile(r"[、][「].*")
_RE_YEAR = re.compile(r"(?:[" + KANJI_BLOCK + "]+)?([0-9?]+|元)年.*")
_RE_BIRTH_DEATH = re.compile(r"(生年不詳|生年月日非公表|生没年不詳).*")
_RE_CURRENT_NAME = re.compile(r"現在の芸名.*")
_RE_KANJI_WIKILINK = re.compile(r"\[\[[" + KANJI_BLOCK + "]+]].*")
_RE_FOREIGN_NAME = re.compile(
    r"(?:英文(名称|表記)|旧名|現姓|旧姓|通称|英文名|原題|ドイツ語|英語|英語表記|英語名称|英文社名|オランダ語|満州語"
    r"|旧|旧芸名|中国語簡体字|漢語名字|略称|本名|英称|英)[:：；;は・].*"
)
_RE_TRAILING_PAREN = re.compile(r"[（:：,]\s*$")
_RE_COMMA_PAREN = re.compile(r"[,、][（:：,]\s*$")
_RE_COMMA_WIKILINK = re.compile(r"[,、]\[\[.*$")
_RE_COMMA_ALPHA = re.compile(r"""[、,][ A-Za-z.'&]+$""")
_RE_COMMA_ALPHA_KANJI2 = re.compile(r"""[、,][ A-Za-z.'-""" + KANJI_BLOCK + """]+$""")
_RE_COMMA_PAREN_ALPHA = re.compile(r"、[（:：\-]*[ A-Za-z]+$")
_RE_COMMA_ABBREV = re.compile(r"、(略称|詳しくは|本名\s*同じ|単に).*$")
_RE_TRAILING_PUNCT = re.compile(r"[？?、－]+\s*$")
_RE_TRAILING_SPACE = re.compile(r"\s*$")
_RE_TRAILING_WIKILINK = re.compile(r"\[\[$")
_RE_WHITESPACE_REMOVE = re.compile(r"\s+")


def is_katakana_or_hiragana_or_nakaguro_or_space(s):
    return bool(KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN.match(s))


def basic_filter(token):
    # &lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;
    token = _RE_LT_REF.sub("", token)

    # <!-- foobar -->
    token = _RE_COMMENT.sub("", token)

    # '''池の平スノーパーク（旧白樺リゾートスキー場）'''（いけのたいらすのーぱーく）
    # '''砂川奈美(旧姓:伊藤)'''（いさがわなみ、[[1991年]][[1月23日]] - ）
    token = _RE_KYUU.sub("", token)
    token = _RE_KYUUSEI.sub("", token)
    token = _RE_DAIME.sub("", token)
    token = _RE_SHODAI.sub("", token)

    # 先頭/末尾の中黒はマークアップ失敗なので、カバーしてあげる
    token = _RE_LEADING_NAKAGURO.sub("", token)
    token = _RE_TRAILING_NAKAGURO.sub("", token)

    token = _RE_AMP.sub("&", token)
    token = _RE_HTML_ENTITY.sub(lambda x: html.unescape(x[1]), token)

    return token.strip()


class Converter:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def convert(self, kanji, yomi) -> (str, str):
        kanji = self.kanji_filter(kanji)
        yomi = self.yomi_filter(kanji, yomi)
        kanji, yomi = hojin_filter(kanji, yomi)
        return kanji, yomi

    def kanji_filter(self, kanji) -> str:
        kanji = basic_filter(kanji)

        # {{lang|en|AMBAC}}
        kanji = _RE_LANG.sub(r"\1", kanji)

        # {{CP932フォント|髙}}千代酒造
        # '''司馬 {{JIS2004フォント|遼󠄁}}太郎'''
        # つじかおり /{{JIS90フォント|辻}}香緒里/
        # {{Anchor|穴子包丁}}
        # うじょう /{{Vanchor|羽状}}/
        # まっちでーじぇいりーぐ /マッチデー{{unicode|♥}}Jリーグ/
        # '''{{linktext|六根}}'''（ろっこん）
        kanji = _RE_TEMPLATE.sub(r"\1", kanji)

        # [[ページ名|リンクラベル]]
        kanji = _RE_WIKILINK_LABEL.sub(r"\1", kanji)
        kanji = _RE_WIKILINK.sub(r"\1", kanji)

        kanji = _RE_WHITESPACE.sub(" ", kanji)

        # '山田 太朗' → 山田太朗
        while True:
            kanji, number_of_subs_made = NAMEISH_PATTERN.subn(r"\1\2", kanji)
            if number_of_subs_made == 0:
                break

        return kanji

    def yomi_filter(self, kanji, yomi):
        yomi = basic_filter(yomi)

        pyomi = yomi
        while True:
            yomi = _RE_NOCHINO.sub("", yomi)
            yomi = _RE_VOICE.sub("", yomi)
            yomi = _RE_YEAR_LINK.sub("", yomi)
            yomi = _RE_DATE_LINK.sub("", yomi)
            yomi = _RE_BOLD.sub("", yomi)
            yomi = _RE_TEMPLATE_OPEN.sub("", yomi)
            yomi = _RE_DATE.sub("", yomi)
            yomi = _RE_QUESTION_DASH.sub("", yomi)
            yomi = _RE_COMMA_ALPHA_KANJI.sub("", yomi)
            yomi = _RE_COMMA_KANJI.sub("", yomi)
            yomi = _RE_COMMA_BRACKET.sub("", yomi)
            yomi = _RE_YEAR.sub("", yomi)
            yomi = _RE_BIRTH_DEATH.sub("", yomi)
            yomi = _RE_CURRENT_NAME.sub("", yomi)
            yomi = _RE_KANJI_WIKILINK.sub("", yomi)
            yomi = _RE_FOREIGN_NAME.sub("", yomi)
            yomi = _RE_TRAILING_PAREN.sub("", yomi)
            yomi = _RE_COMMA_PAREN.sub("", yomi)
            yomi = _RE_COMMA_WIKILINK.sub("", yomi)
            yomi = _RE_COMMA_ALPHA.sub("", yomi)
            yomi = _RE_COMMA_ALPHA_KANJI2.sub("", yomi)
            yomi = _RE_COMMA_PAREN_ALPHA.sub("", yomi)
            yomi = _RE_COMMA_ABBREV.sub("", yomi)
            yomi = _RE_TRAILING_PUNCT.sub("", yomi)
            yomi = _RE_TRAILING_SPACE.sub("", yomi)
            yomi = _RE_TRAILING_WIKILINK.sub("", yomi)

            if pyomi == yomi:
                break
            else:
                pyomi = yomi

        # remove spaces in yomi
        yomi = _RE_WHITESPACE_REMOVE.sub("", yomi)

        yomi = jaconv.kata2hira(yomi)

        yomi = self.filter_yomi_entities(kanji, yomi)

        # アイエスオー、イソ、アイソ to アイエスオー
        if all(is_katakana_or_hiragana_or_nakaguro_or_space(s) for s in yomi.split("、")):
            yomi = yomi.split("、")[0]

        if "、" in yomi:
            yomi = "、".join([s for s in yomi.split("、") if kanji != kanji_normalize(s)])

        return yomi

    def filter_yomi_entities(self, kanji, yomi: str):
        entities = yomi.split("、")

        results = []
        for s in entities:
            # `今鷹 真（今鷹 眞、いまたか まこと 1934年2月28日- ）` のように、旧字体の場合は無視する。
            if kanji_normalize(s) == kanji:
                continue
            if not is_katakana_or_hiragana_or_nakaguro_or_space(s):
                break
            results.append(s)

        # 森ガールの集い（かまいたち、オレンジサンセット、ヒカリゴケ、しゃもじ） みたいなやつはまとめて消す
        # ただし、「しなぬのくにのみやつこ /科野国造/」のような、日本古来の固有名詞に関しては、読み方の揺れが大きいので除外する。
        # '''袁 牧之'''（えん ぼくし、ユエン・ムーチー、ユアン・ムーチー、イエン・ムーツー） みたいなケースも救う
        if len(results) > 3:
            base = results[0]
            if not base.endswith("みやつこ") and not base.startswith("えん"):
                score = mean([Levenshtein.distance(results[0], r) for r in results[1:]])
                if score > 5:
                    self.logger.info("TOOMUCHRESULTS:: " + str(results) + " " + str(score))
                    return ""

        return "、".join(results)
