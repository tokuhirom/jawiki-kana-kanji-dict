#!/usr/bin/env python3
from jawiki.skkdict import merge_skkdict, parse_skkdict, write_skkdict
import logging
import jaconv

# post_validator.py で機械的にはとりのぞきにくいエントリを、このフェーズで除外。

IGNORE_KANJIS = set([
    '雌鳥王', # ヘン https://ja.wikipedia.org/wiki/%E3%83%8F%E3%83%BC%E3%83%A9%E3%83%AB3%E4%B8%96_(%E3%83%87%E3%83%B3%E3%83%9E%E3%83%BC%E3%82%AF%E7%8E%8B)
])

IGNORE_YOMIS = set(
    [
        'てれび',
        'あふがにすたんふんそう',
        'いとうすけのぶ',
        'あなたがいるから',
        'かつ',
        'べーすめんともんすたー',
        'あきお',
        # ありがとう /ARIGATO!/有賀桃/謝謝你，在世界的角落找到我/謝謝你，在世界角落中找到我/
        'ありがとう',
        # らいぶ /Five Colours in Her Hair/LIVE/LiVE/L×I×V×E/Obviously/Room on 3rd Floor/That Girl/The Ballad of Paul K/Ultraviolet/耒部/雷舞/
        'らいぶ',
        # らゔ /LOVE/LOVE Seiko Matsuda 20th Anniversary Best Selection/LUV/Love/LØVE/♥♥♥LOVE♥♥♥/
        'らゔ',
        # いる /109万本/炒る/
        'いる',
        'おーぷにんぐ', # おーぷにんぐ /監督/
        'ぷろぐらみんぐ', # ぷろぐらみんぐ /望月英樹/
        # あめりか /IPTP LLC/NO TOY GETS LEFT BEHIND/ベンジャミン/レコード・ワールド/一般的受容方式/
        'あめりか',
        # さん /ぴろし3/天井/
        'さん',
        # ぼく /お姉さま/繆森/
        'ぼく',
        # 連体詞を除外(mecab-ipadic から抽出)
        # euc-grep 連体詞 Adnominal.csv | perl -pe 's/.*,//' | perl -MLingua::JA::Regular::Unicode=katakana2hiragana -nC -E 'chomp; push @a, katakana2hiragana($_); END { say join ",", map { qq!"$_"! } @a }'
        # かの、ある は除外している。
        "おそるべき", "ざつぜんたる", "ごーごーたる", "さつばつたる", "この", "ただならぬ", "びびたる", "ありし", "いろんな", "ちょっとした", "そーゆう", "もくもくたる", "あまりの", "ちっちゃな", "わが", "そういった", "こんな", "さいたる", "さしたる", "さっそーたる", "くしき", "その", "ある", "わが", "おーきな", "たいした", "かんたる", "あくる", "かくたる", "こーりょーたる", "これらの", "きたる", "いろんな", "どーゆう", "ひょんな", "おそるべき", "ゆゆしき", "れきぜんたる", "れっきとした", "おなじ", "なんたる", "しゃくぜんたる", "どんな", "おんなじ", "そーぜんたる", "ゆーぜんたる", "せいなる", "ひろびろたる", "かかる", "かっこたる", "かくぜんたる", "もーもーたる", "どーどーたる", "りんれつたる", "ちっさな", "おかしな", "おーいなる", "ちちたる", "さる", "およそ", "どの", "おっきな", "しんしんたる", "しかるべき", "おなじ", "たかだか", "いわゆる", "それらの", "ありとあらゆる", "ちーさな", "なき", "せいせいどーどーたる", "たんたんたる", "おーいなる", "かんさんたる", "いかなる", "たいした", "わが", "とーの", "せいぜんたる", "かがやける", "さる", "びびたる", "こーゆう", "だいそれた", "そんな", "たんなる", "こーした", "その", "とんだ", "ちょーぜんたる", "せつせつたる", "なだたる", "そーした", "あんな", "ちーさな", "ろくな", "まんぜんたる", "なんらかの", "たの", "あの", "ばくたる", "しんしんたる", "なんらかの", "ごーごーたる", "しかるべき", "だんぜんたる", "まさかの", "だんこたる", "ふんぜんたる", "ばくぜんたる", "きたる", "みしらぬ", "おーきな", "きぜんたる", "そそたる", "とある", "いかなる", "しゅたる", "おもだった", "かんぜんたる", "ある", "たんなる", "あれらの", "へいぜんたる", "いんぜんたる", "そしらぬ", "さらなる", "あらゆる", "ふとした", "たんぜんたる", "たっての", "げんぜんたる", "ほんの",
        # きどうせんしがんだむてっけつのおるふぇんずげっこう /機動戦士ガンダム鉄血のオルフェンズ月鋼/
        # きどうせんしがんだむのとうじょうじんぶつじおんこうこくぐん /機動戦士ガンダムの登場人物ジオン公国軍/
        # きどうせんしがんだむのとうじょうじんぶつちきゅうれんぽうぐん /機動戦士ガンダムの登場人物地球連邦軍/
        # きどうせんしがんだむのとうじょうじんぶつみんかんじん /機動戦士ガンダムの登場人物民間人/
        'きどうせんしがんだむてっけつのおるふぇんずげっこう',
        'きどうせんしがんだむのとうじょうじんぶつじおんこうこくぐん',
        'きどうせんしがんだむのとうじょうじんぶつちきゅうれんぽうぐん',
        'きどうせんしがんだむのとうじょうじんぶつみんかんじん',
        # あなた /tū, vōs/
        'あなた',
        # きゃっつ /CATS, Cats/
        'きゃっつ',
        # おりじなる /TotheFarSeas -はるかな海へ-/原型/呪われた海/
        'おりじなる',
        # あぷり /じぶん通帳/世紀末麻雀伝説北斗/北斗の拳 〜世紀末麻雀伝説〜/北斗の拳GPS/北斗の拳〜世紀末覇者麻雀バトル〜/北斗の拳スマートショック/北斗の拳早拳伝/
        'あぷり',
        # さんこみっくす /学生たちの道/
        # まーがれっとこみっくす /HEY☆坊や/こんにちはスザンヌ/幸福ゆきかしら?/愛がありますか?/手紙をください!/日の輪月の輪/
        'さんこみっくす',
        'まーがれっとこみっくす',
        # えっくす /400X/EX/○ごとX/
        'えっくす',
        # あるいは /テューキーの補題/ベン・ジョンソン/ホットスポット/
        'あるいは',
        # アーティスト名が入ってきちゃうパターン
        #   ぐりん /夏でSUKA?/
        'ぐりん',
        # '''FANZAアダルトアワード'''（ロゴ・{{lang-en-short|FANZA ADULT AWARD}}）
        'ろご',
        # バンドのメンバー紹介項目を除外
        # ぎたー /8P/AYA/Aki/CAT/EBBY/EDDIE/GAK/GENTA/
        'ぎたー',
        'どらむ',
        'きーぼーど',
        'ぴあの',
        'べーす',
        'ぼーかる',
        'ぷろでゅーす',
        'ひろいん',
        'ばす',
        'どらむす',
        'てのーる',
        'さっくす',
        'あこーでぃおん',
        'げすと',
        'いんすとぅるめんたる',
        'いんでぃぺんでんとれーべる',
        'おるがん',
        'そぷらの',
        'ゔぃおら',
        'いんでぃーず',
        # さんばーすと /Gibson Les Paul Standard 1959 Historic Collection/
        'さんばーすと',
        # かまいたち /ひびきすぎ夫/伝令係・谷/森ガールの集い/
        'かまいたち',
        # いいか /Then, for the thousands in attendance, and the millions watching at home./
        'いいか',
        # ゑい /優勝内国産馬連合競走/長谷川榮/
        'ゑい',
        # うち /86校/死者273人/死者・行方不明者約2万2000人/
        'うち',
        # および /UTF-32/江迎警察署 - 北部/相補誤差関数/
        'および',
        # あばんたいとる /監督/
        'あばんたいとる',
        # えすか /擬餌状体/銀河刑務所の囚人を全員脱獄させる。/
        'えすか',
        # ぐらびああいどる /寺口智香/愛心/
        'ぐらびああいどる',
        # おぷしょん /OPTION/作者情報/名前/
        'おぷしょん',
        # こんと /戦え!動物戦士ももいろアニマルZ 本編
        'こんと',
        # げーむぼーいからー /JリーグエキサイトステージGB/
        'げーむぼーいからー',
        # あこーすてぃっく /TheEnd/
        'あこーすてぃっく',
        # または /イルーニャ/インターラーケン修道院/カットアップ/
        'または',
        # ぼーなすとらっく /AllYouMiss/AnswertoThisFlower/CircleofLife/DreamingStar/Ican'tfollowyou/KeepInThePockets[Remix]/
        'ぼーなすとらっく',
        # あむすてるだむ /IPTP Limited/オランダのコーヒーショップ/
        # '''IPTP Limited'''（アムステルダム、ホラン）
        'あむすてるだむ',
        # おりじなるからおけ /APlaceUndertheSun/BoomBoomMyHeart〈TVMIX〉/CHEERSFORYOU/Darlin'/GETLOVE/HERO/HERO（アカペラバージョン）/
        'おりじなるからおけ',
        'からおけ',
        'あんこーる',
        # ''CSS等の保護技術を回避してのDVDのリッピングは私的複製の対象外となり違法行為となる'''（ただし、CSS等の保護技術が使われていないDVDのリッピングについては、改正後も従来と変わりはない）
        'ただし',
        # だぶるぜーたばーじょん Chai Maxx -ZZ ver.-,DNA狂詩曲 -ZZ ver.-,GOUNN -ZZ ver.-,MOON PRIDE -ZZ ver.-,Moon Revenge -ZZ ver.-,My Dear Fellow -ZZ ver.-,ZZ ver.,全力少女 -ZZ ver.-,月虹 -ZZ ver.-,白い風 -ZZ ver.-
        'だぶるぜーたばーじょん',
        # きょうのほんこん /今日の香港、明日の台湾、明後日の沖縄/
        # きょうのほんこんあすのたいわん /今日の香港、明日の台湾/
        'きょうのほんこん',
        'きょうのほんこんあすのたいわん',
        # こっくえき /谷口駅/
        'こっくえき',
        # うえいとれす /野村和子/
        'うえいとれす',
    ])


def read_filtered(fname):
    result = {}

    with open(fname, 'r', encoding='utf-8') as ifh:
        for line in ifh:
            kanji, yomi = line.strip().split("\t")
            if yomi not in result:
                result[yomi] = []
            result[yomi].append(kanji)

    return result


def preproc(dic, skkdict):
    for y in IGNORE_YOMIS:
        dic.pop(y, None)

    # remove entries in skk dict.
    for yomi in sorted(dic.keys()):
        dic[yomi] = [kanji for kanji in sorted(set(dic[yomi])) if not should_skip(kanji, yomi, skkdict)]

    return dic


def should_skip(kanji, yomi, skkdict):
    if yomi not in skkdict:
        return False

    if kanji in skkdict[yomi]:
        return True

    if kanji in IGNORE_KANJIS:
        return True

    # おめが /冥王計画ゼオライマーΩ/闘神都市Ω/
    # のようなケースを除外する
    for skk_kanji in skkdict[yomi]:
        if skk_kanji in kanji and skk_kanji != kanji:
            logging.debug("skipped entry: yomi=%s skk_kanji=%s kanji=%s" % (yomi, skk_kanji, kanji))
            return True

    # 読みの方が短いものは除去する
    if len(kanji) > len(yomi):
        return True

    return False


def write_mecabdic(dictname, dictionary, score=4569):
    with open(dictname, 'w', encoding='utf-8') as ofp:
        # 東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
        for yomi in sorted(dictionary.keys()):
            # ',' が入っているものがあると、CSV として壊れるので無視する
            if ',' in yomi:
                continue

            for kanji in dictionary[yomi]:
                # ',' が入っているものがあると、CSV として壊れるので無視する
                if ',' in kanji:
                    continue
                ofp.write(f"{kanji},1288,1288,{score},名詞,固有名詞,一般,*,*,*,{kanji},{yomi},{yomi}\n")

def write_linderadic(dictname, dictionary):
    # https://github.com/lindera-morphology/lindera
    with open(dictname, 'w', encoding='utf-8') as ofp:
        # 東京スカイツリー,カスタム名詞,トウキョウスカイツリー
        for yomi in sorted(dictionary.keys()):
            # ',' が入っているものがあると、CSV として壊れるので無視する
            if ',' in yomi:
                continue

            for kanji in dictionary[yomi]:
                # ',' が入っているものがあると、CSV として壊れるので無視する
                if ',' in kanji:
                    continue
                ofp.write(f"{kanji},カスタム名詞,{jaconv.hira2kata(yomi)}\n")


if __name__ == '__main__':
    import sys
    import time

    logging.basicConfig(level=logging.INFO)

    t0 = time.time()

    skkdicts = [parse_skkdict(path, encoding='euc-jp') for path in sys.argv[1:]]
    skkdict = merge_skkdict(skkdicts)

    result = read_filtered('dat/post_validated.tsv')
    result = preproc(result, skkdict)
    write_skkdict('SKK-JISYO.jawiki', result)
    write_mecabdic('mecab-userdic.csv', result)
    write_linderadic('lindera-userdic.csv', result)

    logging.info("Scanned: {0} seconds".format(time.time()-t0))
