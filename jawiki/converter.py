import logging
import re
import jaconv
from jawiki.hojin import hojin_filter
from statistics import mean
import Levenshtein
import html
from jawiki.jachars import HIRAGANA_BLOCK, KANJI_BLOCK, KATAKANA_BLOCK, kanji_normalize

NAMEISH_PATTERN = re.compile(
    r'([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)' +
    '[\u0020\u3000]+([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)'
)

KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN = \
    re.compile(r'^[ 　' + KATAKANA_BLOCK + HIRAGANA_BLOCK + '・]+$')

def is_katakana_or_hiragana_or_nakaguro_or_space(s):
    return bool(KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN.match(s))

def basic_filter(token):
    token = re.sub(r'&lt;ref.*|&lt;!--.*--&gt;', '', token)
    token = re.sub(r'（旧.*?）|[（\(](旧姓|本名)[:：].*?[）\)]|（(\d+|[一-九])代目?）|（初代）', '', token)
    token = re.sub(r'^・|・$', '', token)
    token = re.sub(r'&amp;', r'&', token)
    token = re.sub(r'(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)', lambda x: html.unescape(x[1]), token)
    return token.strip()

class Converter:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def convert(self, kanji, yomi) -> (str, str):
        kanji = self.kanji_filter(kanji)
        yomi = self.yomi_filter(kanji, yomi)
        return hojin_filter(kanji, yomi)

    def kanji_filter(self, kanji) -> str:
        kanji = basic_filter(kanji)
        kanji = re.sub(r'\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}', r'\1', kanji)
        kanji = re.sub(r'\{\{(?:En|IPA-en|要出典範囲|linktext|unicode|Anchor|Vanchor|[A-Z0-9]+フォント)\|(.+)\}\}', r'\1', kanji)
        kanji = re.sub(r'\[\[(?:.*)\|(.*)\]\]|\[\[(.*)\]\]', r'\1', kanji)
        kanji = re.sub(r'\s+', r' ', kanji)

        while True:
            kanji, number_of_subs_made = re.subn(NAMEISH_PATTERN, r'\1\2', kanji)
            if number_of_subs_made == 0:
                break

        return kanji

    def yomi_filter(self, kanji, yomi):
        yomi = basic_filter(yomi)
        pyomi = yomi

        while True:
            yomi = re.sub(r"^のちの('''|\[\[).*|、声 - .*|\[\[\d+年\]\].*|\[\[\d+月\d+日\]\].*|''.*|\{\{.*|\d+月\d+日.*|\?\s*-\s*$", '', yomi)
            yomi = re.sub(r'[、][a-zA-Z]+[' + KANJI_BLOCK + ']+$|[、][' + KANJI_BLOCK + ']+$|[、][「].*', '', yomi)
            yomi = re.sub(r'(?:[' + KANJI_BLOCK + ']+)?([0-9?]+|元)年.*|(生年不詳|生年月日非公表|生没年不詳).*|現在の芸名.*|\[\[[' + KANJI_BLOCK + ']+]].*', '', yomi)
            yomi = re.sub(r'(?:英文(名称|表記)|旧名|現姓|旧姓|通称|英文名|原題|ドイツ語|英語|英語表記|英語名称|英文社名|オランダ語|満州語|旧|旧芸名|中国語簡体字|漢語名字|略称|本名|英称|英)[:：；;は・].*', '', yomi)
            yomi = re.sub(r'[（:：,]\s*$|[,、][（:：,]\s*$|[,、]\[\[.*$|[、,][ A-Za-z.'&]+$|[、,][ A-Za-z.'-]' + KANJI_BLOCK + ']+$|、[（:：\-]*[ A-Za-z]+$|、(略称|詳しくは|本名\s*同じ|単に).*|[？?、－]+\s*$|\s*$|\[\[$', '', yomi)

            if pyomi == yomi:
                break
            else:
                pyomi = yomi

        yomi = re.sub(r'\s+', r'', yomi)
        yomi = jaconv.kata2hira(yomi)
        yomi = self.filter_yomi_entities(kanji, yomi)

        if all([is_katakana_or_hiragana_or_nakaguro_or_space(s) for s in yomi.split('、')]):
            yomi = yomi.split('、')[0]

        if '、' in yomi:
            yomi = "、".join([s for s in yomi.split('、') if kanji != kanji_normalize(s)])

        return yomi

    def filter_yomi_entities(self, kanji, yomi: str):
        entities = yomi.split('、')
        results = [s for s in entities if kanji_normalize(s) != kanji and is_katakana_or_hiragana_or_nakaguro_or_space(s)]

        if len(results) > 3:
            base = results[0]
            if not base.endswith('みやつこ') and not base.startswith('えん'):
                score = mean([Levenshtein.distance(results[0], r) for r in results[1:]])
                if score > 5:
                    self.logger.info("TOOMUCHRESULTS:: " + str(results) + ' ' + str(score))
                    return ''

        return '、'.join(results)
