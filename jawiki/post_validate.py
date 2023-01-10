import logging
import re
from typing import Optional

import jaconv
import romkan

from jawiki.jachars import HIRAGANA_BLOCK, KATAKANA_BLOCK, \
    is_hiragana, HIRAGANA_NORMALIZER, \
    normalize_hiragana

INVALID_KANJI_PATTERNS = [
    # 9代式守伊之助
    re.compile(r'^\d+(月|世紀|年代|代|年)'),
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
    # 曖昧さ回避のためのページで、
    # 日本(ごうしゅう)という表記がある。
    # https://ja.wikipedia.org/wiki/%E6%B1%9F%E5%B7%9E
    re.compile(r'^(日本|中国|韓国)$'),
]


class PostValidator:

    def __init__(self, tokenizer, logger=logging.getLogger(__name__)):
        self.tokenizer = tokenizer
        self.logger = logger

    def post_validate(self, kanji, yomi) -> Optional[str]:
        msg = self.__validate_basic(kanji, yomi)
        if msg:
            return msg

        msg = self.__validate_with_janome(kanji, yomi)
        if msg:
            return msg

        return None

    def __validate_basic(self, kanji, yomi):
        if len(kanji) == 0:
            return 'kanji is empty'

        if len(kanji) == 1:
            return 'kanji is single character'

        if len(yomi) == 0:
            return 'yomi is empty'

        if len(yomi) < 2:
            return f'yomi is too short! {len(yomi)}<2'

        if len(romkan.to_roma(yomi)) * 1.5 < len(kanji):
            return 'yomi is too short...'

        if not is_hiragana(yomi):
            return 'yomi contains non-hiragana char'

        if is_hiragana(kanji):
            return 'kanji is hiragana'

        for kanji_prefix in ['〜', '『', '「', '＜', '〈', '《', '／', '日本の']:
            if kanji.startswith(kanji_prefix):
                return f'kanji starts with {kanji_prefix}'

        for kanji_postfix in ['・']:
            if kanji.endswith(kanji_postfix):
                return f'kanji ends with {kanji_postfix}'

        for yomi_prefix in [
            # '''[[マイクロソフト]]'''（ただし、[[Xbox 360]]はどちらの規格にも対応せず、[[Microsoft Windows Vista]]は両規格に対応していた）
            'ただし、',
            # この音は'''ハーフ・ストップ'''（あるいはエコー、ハーフ・ミュート）と呼ばれる。
            'あるいは',
            'おりんぴっくの',
        ]:
            if yomi.startswith(yomi_prefix):
                return f'yomi starts with {yomi_prefix}'

        # yomi infx
        for yomi_infix in [
            # ''w3m'''（ダブリューサンエム または ダブリュースリーエム）
            ' または ',
            'における',
            'あるいは',
            "'''",
            '[',
        ]:
            if yomi_infix in yomi:
                return f'yomi contains {yomi_infix}'

        # kanji infix
        for kanji_infix in [
            # '''Keyboard / kAoru ikArAshi / 五十嵐 馨'''（いからし かおる）
            '/',
            "''",
            '{{',
            '[[',
            '(',
            '（',
        ]:
            if kanji_infix in kanji:
                return f'kanji contains {kanji_infix}'

        for pattern in INVALID_KANJI_PATTERNS:
            if pattern.match(kanji):
                return f'Invalid kanji pattern: {pattern}'

        # katakana prefix
        normalized_yomi = normalize_hiragana(yomi)
        m = re.match(r'^([' + KATAKANA_BLOCK + ']+)', kanji)
        if m:
            prefix = m[1]
            prefix_hira = normalize_hiragana(jaconv.kata2hira(prefix))
            if not normalized_yomi.startswith(prefix_hira):
                return f"Kanji prefix and yomi prefix aren't same: normalized_yomi={normalized_yomi}" \
                       f" prefix_hira={prefix_hira}"

        # '''大切な者との記憶'''（キューブ） のようなものを除外。
        for k in re.findall(r'([' + HIRAGANA_BLOCK + ']+)', kanji):
            k = normalize_hiragana(k)
            if k not in normalized_yomi:
                return f"kana yomi and kanji missmatch: normalized_yomi={normalized_yomi}, k={k}"

        # katakana postfix
        m = re.match(r'.*?([' + KATAKANA_BLOCK + ']+)$', kanji)
        if m:
            postfix = m[1]
            postfix_hira = jaconv.kata2hira(postfix).translate(HIRAGANA_NORMALIZER)
            normalized_yomi = yomi.translate(HIRAGANA_NORMALIZER)
            if not normalized_yomi.endswith(postfix_hira):
                return (
                    f"Kanji postfix and yomi postfix aren't same: normalized_yomi={normalized_yomi} "
                    f"postfix_hira={postfix_hira}")

        m = re.match(r'^([' + HIRAGANA_BLOCK + KATAKANA_BLOCK + ']+)$', kanji)
        if m:
            if normalize_hiragana(jaconv.kata2hira(yomi)) != normalize_hiragana(jaconv.kata2hira(kanji)):
                return "Kanji != Kana"

        return None

    # うちゅうけいじたましい /宇宙刑事魂 THE SPACE SHERIFF SPIRITS/
    # のようなケースを除外したい。
    def __validate_with_janome(self, kanji, yomi):
        # しくらちよまる /志倉千代丸/ が、「こころざしくらちよまる」になるケースを特別に除外する
        # きしなみかお /岸波香桜/ -> *きしなみかお*りさくら
        # くらちれお /倉知玲鳳/ -> *くらちれお*おとり
        for c in ['志', '香', '鳳']:
            if c in kanji:
                return None

        janome_yomi = jaconv.kata2hira(''.join(
            [n.reading if str(n.reading) != '*' else n.base_form for n in self.tokenizer.tokenize(kanji)]))
        normalized_janome_yomi = normalize_hiragana(janome_yomi)
        normalized_yomi = normalize_hiragana(yomi)

        self.logger.debug(f"yomi={yomi} normalized_yomi={normalized_yomi}, janome_yomi={janome_yomi},"
                          f" normalized_janome_yomi={normalized_janome_yomi}")
        if normalized_yomi in normalized_janome_yomi:
            extra = len(re.sub(normalized_yomi, '', normalized_janome_yomi, 1))

            # 2 に意味はない。
            # 愛植男=あいうえお が janome だと あいうえおとこ になるのの救済をしている。
            if extra > 3:
                return f"kanji may contain extra chars(janome): janome_yomi={janome_yomi}"
            else:
                return None

        return None
