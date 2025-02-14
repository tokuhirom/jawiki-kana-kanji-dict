import logging
import re
import html
from statistics import mean

import jaconv
import Levenshtein

from jawiki.hojin import hojin_filter
from jawiki.jachars import HIRAGANA_BLOCK, KANJI_BLOCK, KATAKANA_BLOCK, kanji_normalize

NAMEISH_PATTERN = re.compile(
    r'([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)' +
    r'[\u0020\u3000]+([' + HIRAGANA_BLOCK + KANJI_BLOCK + KATAKANA_BLOCK + ']+)'
)

KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN = re.compile(r'^[ 　' + KATAKANA_BLOCK + HIRAGANA_BLOCK + '・]+$')


def is_katakana_or_hiragana_or_nakaguro_or_space(s):
    return bool(KATAKANA_OR_HIRAGANA_OR_NAKAGURO_OR_SPACE_PATTERN.match(s))


def basic_filter(token):
    token = re.sub(r'&lt;ref.*', '', token)
    token = re.sub(r'&lt;!--.*--&gt;', '', token)
    token = re.sub(r'（旧.*?）', '', token)
    token = re.sub(r'[（\(](旧姓|本名)[:：].*?[）\)]', '', token)
    token = re.sub(r'（(\d+|[一-九])代目?）', '', token)
    token = re.sub(r'（初代）', '', token)
    token = re.sub(r'^・', '', token)
    token = re.sub(r'・$', '', token)
    token = re.sub(r'&amp;', '&', token)
    token = re.sub(r'(&(?:[a-z_-]+|#[0-9]+|#x[0-9A-Fa-f]+);)', lambda x: html.unescape(x[1]), token)
    return token.strip()


class Converter:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def convert(self, kanji, yomi):
        kanji = self.kanji_filter(kanji)
        yomi = self.yomi_filter(kanji, yomi)
        kanji, yomi = hojin_filter(kanji, yomi)
        return kanji, yomi

    def kanji_filter(self, kanji):
        kanji = basic_filter(kanji)
        kanji = re.sub(r'\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}', r'\1', kanji)
        kanji = re.sub(r'\{\{(?:En|IPA-en|要出典範囲|linktext|unicode|Anchor|Vanchor|[A-Z0-9]+フォント)\|(.+)\}\}', r'\1', kanji)
        kanji = re.sub(r'\[\[(?:.*)\|(.*)\]\]', r'\1', kanji)
        kanji = re.sub(r'\[\[(.*)\]\]', r'\1', kanji)
        kanji = re.sub(r'\s+', ' ', kanji)
        while True:
            kanji, number_of_subs_made = re.subn(NAMEISH_PATTERN, r'\1\2', kanji)
            if number_of_subs_made == 0:
                break
        return kanji

    def yomi_filter(self, kanji, yomi):
        yomi = basic_filter(yomi)
        previous_yomi = yomi
        while True:
            yomi = re.sub(r"^のちの('''|\[\[).*", '', yomi)
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
            yomi = re.sub(
                r'(?:英文(名称|表記)|旧名|現姓|旧姓|通称|英文名|原題|ドイツ語|英語|英語表記|英語名称|英文社名|オランダ語|満州語'
                r'|旧|旧芸名|中国語簡体字|漢語名字|略称|本名|英称|英)[:：；;は・].*',
                '', yomi)
            yomi = re.sub(r'[（:：,]\s*$', '', yomi)
            yomi = re.sub(r'[,、][（:：,]\s*$', '', yomi)
            yomi = re.sub(r'[,、]\[\[.*$', '', yomi)
            yomi = re.sub(r'''[、,][ A-Za-z.'&]+$''', '', yomi)
            yomi = re.sub(r'''[、,][ A-Za-z.'-''' + KANJI_BLOCK + ''']+$''', '', yomi)
            yomi = re.sub(r'、[（:：\-]*[ A-Za-z]+$', '', yomi)
            yomi = re.sub(r'、(略称|詳しくは|本名\s*同じ|単に).*$', '', yomi)
            yomi = re.sub(r'[？?、－]+\s*$', '', yomi)
            yomi = re.sub(r'\s*$', '', yomi)
            yomi = re.sub(r'\[\[$', '', yomi)

            if previous_yomi == yomi:
                break
            else:
                previous_yomi = yomi

        yomi = re.sub(r'\s+', '', yomi)
        yomi = jaconv.kata2hira(yomi)
        yomi = self.filter_yomi_entities(kanji, yomi)

        if all(is_katakana_or_hiragana_or_nakaguro_or_space(s) for s in yomi.split('、')):
            yomi = yomi.split('、')[0]

        if '、' in yomi:
            yomi = "、".join(s for s in yomi.split('、') if kanji != kanji_normalize(s))

        return yomi

    def filter_yomi_entities(self, kanji, yomi):
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
