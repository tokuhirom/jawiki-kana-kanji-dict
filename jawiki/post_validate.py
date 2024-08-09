import logging
import re
from typing import Optional

import jaconv
from jawiki.romkan import to_roma

from jawiki.jachars import HIRAGANA_BLOCK, KATAKANA_BLOCK, \
    is_hiragana, HIRAGANA_NORMALIZER, \
    normalize_hiragana

INVALID_KANJI_PATTERNS = [
    # 9代式守伊之助
    re.compile(r'^\d+(月|世紀|年代|代|年)'),
    # 三代目尾上菊五郎
    re.compile(r'^(.代目|初代)'),
    # 第42回NHK紅白歌合戦
    re.compile(r'^第\d+回'),
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
    # 国名 + "の" + 名詞、のパターンを除外。単語ではないので。
    #
    #   うくらいなのうちゅうかいはつ /ウクライナの宇宙開発/
    #   うくらいなのえいゆうとし /ウクライナの英雄都市/
    #   うくらいなのかとりっくきょうかい /ウクライナのカトリック教会/
    #   うくらいなのげいじゅつ /ウクライナの芸術/
    #   うくらいなのこっか /ウクライナの国歌/
    #   うくらいなのこっき /ウクライナの国旗/
    #   うくらいなのしゅしょう /ウクライナの首相/
    #   うくらいなのせいじ /ウクライナの政治/
    #   うくらいなのせかいいさん /ウクライナの世界遺産/
    #   うくらいなのだいとうりょう /ウクライナの大統領/
    #   うくらいなのちり /ウクライナの地理/
    #   うくらいなのてつどう /ウクライナの鉄道/
    re.compile(r'^.*の(宇宙開発|英雄都市|芸術|国家|国旗|首相|副首相|政治|世界遺産|大統領|副大統領|地理|鉄道|州|宗教|人種差別|選挙|戦争犯罪|地域|歴史|交通|核実験|国会|舞踊|数学|美術|仏教|旗|地方|地域区分|地方政府|日本語教育|総督|政党|地域対立|ユーロ硬貨|首長|県|教育|音楽|都市|鉄道事故|経済史|国道|国立公園|少数民族|伝統音楽|民間療法|電話番号|大量破壊兵器|祝日)$'),
    # 相生市立矢野小学校 のようなケースを除外する
    # ○○県立○○は、辞書に登録すべき表現ではない。
    # 分割して登録されるべき。。
    # 変換するときにも、県立、とかつけずに変換することが多いだろう。
    re.compile(r'^.*[市区町村都道府県]立.*(学校|分校|大学|高校|図書館|美術館|科学館|植物園|博物館|キャンパス|文学館|センター|学園|病院|公園|ホール|競技場|歴史館|資料館)$'),
    re.compile(r'^.*[都道府県]の(観光地|高校入試|資格者配置路線|城|記念物|ワイン|石材用手押軌道群|高校野球|ラーメン|人口統計|年表|暴力団|苗字|高等学校設立年表|年中行事|花街道|文学史)$'),
    re.compile(r'^.*(に関する特別措置法|に関する政令|を提供する法律|との間の協定|ニ関スル法律|に関する省令|を改正する法律)$'),
    re.compile(r'^地域医療連携推進法人.+$'),
    # https://github.com/tokuhirom/jawiki-kana-kanji-dict/issues/20
    re.compile(r'^.*のゲーム$'),
    re.compile(r'^.*の用語$'),
    # ししょうしりーずししょうとぼくと /師匠シリーズ 〜師匠と僕と〜/
    re.compile(r'^.*〜.*〜.*$'),
    # のろわれたむら /呪われた村<ジェルサレムズ・ロット>/
    re.compile(r'.*[<>].*'),
]


class PostValidator:

    def __init__(self, tokenizer, logger=logging.getLogger(__name__)):
        self.tokenizer = tokenizer
        self.logger = logger

    def post_validate(self, kanji, yomi) -> Optional[str]:
        msg = self.__validate_basic(kanji, yomi)
        if msg:
            return msg

        msg = self.__validate_with_jaconv(kanji, yomi)
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

        if len(yomi) >= 20:
            # データを見た限り、読みが20文字を超えるものは
            # 複合語しかない。
            #
            # きゃぷてんつばさせかいだいけっせんじゅにあわーるどかっぷ /キャプテン翼世界大決戦!! Jr.ワールドカップ/
            # など。
            return f'yomi is tooooo long! {len(yomi)}<2'

        if len(to_roma(yomi)) * 1.5 < len(kanji):
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
    def __validate_with_jaconv(self, kanji, yomi):
        # しくらちよまる /志倉千代丸/ が、「こころざしくらちよまる」になるケースを特別に除外する
        # きしなみかお /岸波香桜/ -> *きしなみかお*りさくら
        # くらちれお /倉知玲鳳/ -> *くらちれお*おとり
        for c in ['志', '香', '鳳']:
            if c in kanji:
                return None

        jaconv_yomi = jaconv.kata2hira(''.join(
            [n.reading if str(n.reading) != '*' else n.base_form for n in self.tokenizer.tokenize(kanji)]))
        normalized_jaconv_yomi = normalize_hiragana(jaconv_yomi)
        normalized_yomi = normalize_hiragana(yomi)

        self.logger.debug(f"yomi={yomi} normalized_yomi={normalized_yomi}, jaconv_yomi={jaconv_yomi},"
                          f" normalized_jaconv_yomi={normalized_jaconv_yomi}")
        if normalized_yomi in normalized_jaconv_yomi:
            extra = len(re.sub(normalized_yomi, '', normalized_jaconv_yomi, 1))

            # 2 に意味はない。
            # 愛植男=あいうえお が jaconv だと あいうえおとこ になるのの救済をしている。
            if extra > 3:
                return f"kanji may contain extra chars(jaconv): jaconv_yomi={jaconv_yomi}"
            else:
                return None

        return None
