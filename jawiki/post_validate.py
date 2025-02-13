import logging
import re
from typing import Optional

import jaconv
from jawiki.romkan import to_roma
from jawiki.jachars import (
    HIRAGANA_BLOCK, KATAKANA_BLOCK, is_hiragana,
    HIRAGANA_NORMALIZER, normalize_hiragana
)

# Compile regex patterns only once at module level
INVALID_KANJI_PATTERNS = [
    re.compile(pattern) for pattern in [
        r'^\d+(月|世紀|年代|代|年)',
        r'^(.代目|初代)',
        r'^第\d+回',
        r'^[0-9]+$',
        r'^[0-9]+\.『',
        r'\{\{仮リンク',
        r'^日本の企業一覧',
        r'.*の登場(?:人物|キャラクター|仮面ライダー|怪獣|メカ|兵器|組織|馬|人物一覧|レスラー|人物の索引)$',
        r'第\d+話',
        r'^(日本|中国|韓国)$',
        r'^.*の(宇宙開発|英雄都市|芸術|国家|国旗|首相|副首相|政治|世界遺産|大統領|副大統領|地理|鉄道|州|宗教|人種差別|選挙|戦争犯罪|地域|歴史|交通|核実験|国会|舞踊|数学|美術|仏教|旗|地方|地域区分|地方政府|日本語教育|総督|政党|地域対立|ユーロ硬貨|首長|県|教育|音楽|都市|鉄道事故|経済史|国道|国立公園|少数民族|伝統音楽|民間療法|電話番号|大量破壊兵器|祝日)$',
        r'^.*[市区町村都道府県]立.*(学校|分校|大学|高校|図書館|美術館|科学館|植物園|博物館|キャンパス|文学館|センター|学園|病院|公園|ホール|競技場|歴史館|資料館)$',
        r'^.*[都道府県]の(観光地|高校入試|資格者配置路線|城|記念物|ワイン|石材用手押軌道群|高校野球|ラーメン|人口統計|年表|暴力団|苗字|高等学校設立年表|年中行事|花街道|文学史)$',
        r'^.*(に関する特別措置法|に関する政令|を提供する法律|との間の協定|ニ関スル法律|に関する省令|を改正する法律)$',
        r'^地域医療連携推進法人.+$',
        r'^.*のゲーム$',
        r'^.*の用語$',
        r'^.*〜.*〜.*$',
        r'.*[<>].*'
    ]
]

INVALID_YOMI_PREFIXES = ['ただし、', 'あるいは', 'おりんぴっくの']
INVALID_YOMI_INFIXES = [' または ', 'における', 'あるいは', "'''", '[']
INVALID_KANJI_INFIXES = ['/', "''", '{{', '[[', '(', '（']
INVALID_KANJI_PREFIXES = ['〜', '『', '「', '＜', '〈', '《', '／', '日本の']
INVALID_KANJI_POSTFIXES = ['・']
SPECIAL_KANJI_CHARS = ['志', '香', '鳳']

class PostValidator:
    def __init__(self, tokenizer, logger=logging.getLogger(__name__)):
        self.tokenizer = tokenizer
        self.logger = logger

    def post_validate(self, kanji: str, yomi: str) -> Optional[str]:
        """Validates kanji and yomi pair, returns error message if invalid."""
        if error := self._validate_basic(kanji, yomi):
            return error
        return self._validate_with_jaconv(kanji, yomi)

    def _validate_basic(self, kanji: str, yomi: str) -> Optional[str]:
        """Performs basic validation checks on kanji and yomi."""
        # Length checks
        if not kanji:
            return 'kanji is empty'
        if len(kanji) == 1:
            return 'kanji is single character'
        if not yomi:
            return 'yomi is empty'
        if len(yomi) < 2:
            return f'yomi is too short! {len(yomi)}<2'
        if len(yomi) >= 20:
            return f'yomi is tooooo long! {len(yomi)}<2'
        if len(to_roma(yomi)) * 1.5 < len(kanji):
            return 'yomi is too short...'

        # Character type checks
        if not is_hiragana(yomi):
            return 'yomi contains non-hiragana char'
        if is_hiragana(kanji):
            return 'kanji is hiragana'

        # Prefix/postfix/infix checks
        for prefix in INVALID_KANJI_PREFIXES:
            if kanji.startswith(prefix):
                return f'kanji starts with {prefix}'
        for postfix in INVALID_KANJI_POSTFIXES:
            if kanji.endswith(postfix):
                return f'kanji ends with {postfix}'
        for prefix in INVALID_YOMI_PREFIXES:
            if yomi.startswith(prefix):
                return f'yomi starts with {prefix}'
        for infix in INVALID_YOMI_INFIXES:
            if infix in yomi:
                return f'yomi contains {infix}'
        for infix in INVALID_KANJI_INFIXES:
            if infix in kanji:
                return f'kanji contains {infix}'

        # Pattern checks
        for pattern in INVALID_KANJI_PATTERNS:
            if pattern.match(kanji):
                return f'Invalid kanji pattern: {pattern}'

        # Katakana prefix/postfix validation
        normalized_yomi = normalize_hiragana(yomi)
        if error := self._validate_katakana(kanji, normalized_yomi):
            return error

        # Hiragana validation
        for k in re.findall(f'[{HIRAGANA_BLOCK}]+', kanji):
            k = normalize_hiragana(k)
            if k not in normalized_yomi:
                return f"kana yomi and kanji missmatch: normalized_yomi={normalized_yomi}, k={k}"

        # Full kana validation
        if re.match(f'^[{HIRAGANA_BLOCK}{KATAKANA_BLOCK}]+$', kanji):
            if normalize_hiragana(jaconv.kata2hira(yomi)) != normalize_hiragana(jaconv.kata2hira(kanji)):
                return "Kanji != Kana"

        return None

    def _validate_katakana(self, kanji: str, normalized_yomi: str) -> Optional[str]:
        """Validates katakana components in kanji against normalized yomi."""
        if prefix_match := re.match(f'^([{KATAKANA_BLOCK}]+)', kanji):
            prefix = prefix_match[1]
            prefix_hira = normalize_hiragana(jaconv.kata2hira(prefix))
            if not normalized_yomi.startswith(prefix_hira):
                return f"Kanji prefix and yomi prefix aren't same: normalized_yomi={normalized_yomi} prefix_hira={prefix_hira}"

        if postfix_match := re.match(f'.*?([{KATAKANA_BLOCK}]+)$', kanji):
            postfix = postfix_match[1]
            postfix_hira = normalize_hiragana(jaconv.kata2hira(postfix))
            if not normalized_yomi.endswith(postfix_hira):
                return f"Kanji postfix and yomi postfix aren't same: normalized_yomi={normalized_yomi} postfix_hira={postfix_hira}"

        return None

    def _validate_with_jaconv(self, kanji: str, yomi: str) -> Optional[str]:
        """Validates kanji and yomi using jaconv conversion."""
        if any(c in kanji for c in SPECIAL_KANJI_CHARS):
            return None

        tokenized_readings = [n.reading if str(n.reading) != '*' else n.base_form for n in self.tokenizer.tokenize(kanji)]
        jaconv_yomi = jaconv.kata2hira(''.join(tokenized_readings))
        normalized_jaconv_yomi = normalize_hiragana(jaconv_yomi)
        normalized_yomi = normalize_hiragana(yomi)

        self.logger.debug(f"yomi={yomi} normalized_yomi={normalized_yomi}, jaconv_yomi={jaconv_yomi}, normalized_jaconv_yomi={normalized_jaconv_yomi}")

        if normalized_yomi in normalized_jaconv_yomi:
            extra_chars = len(re.sub(normalized_yomi, '', normalized_jaconv_yomi, 1))
            return f"kanji may contain extra chars(jaconv): jaconv_yomi={jaconv_yomi}" if extra_chars > 3 else None

        return None