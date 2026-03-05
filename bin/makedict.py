#!/usr/bin/env python3
from jawiki.skkdict import merge_skkdict, parse_skkdict, write_skkdict
import logging

# post_validator.py で機械的にはとりのぞきにくいエントリを、このフェーズで除外。

IGNORE_KANJIS = {
    "雌鳥王",  # ヘン https://ja.wikipedia.org/wiki/%E3%83%8F%E3%83%BC%E3%83%A9%E3%83%AB3%E4%B8%96_(%E3%83%87%E3%83%B3%E3%83%9E%E3%83%BC%E3%82%AF%E7%8E%8B)
}

IGNORE_YOMIS = {
    "あきお",
    "あくる",
    # あこーすてぃっく /TheEnd/
    "あこーすてぃっく",
    "あこーでぃおん",  # バンドのメンバー紹介項目
    # あなた /tū, vōs/
    "あなた",
    "あなたがいるから",
    "あの",
    # あばんたいとる /監督/
    "あばんたいとる",
    "あふがにすたんふんそう",
    # あぷり /じぶん通帳/世紀末麻雀伝説北斗/北斗の拳 〜世紀末麻雀伝説〜/北斗の拳GPS/北斗の拳〜世紀末覇者麻雀バトル〜/北斗の拳スマートショック/北斗の拳早拳伝/
    "あぷり",
    "あまりの",
    # あむすてるだむ /IPTP Limited/オランダのコーヒーショップ/
    # '''IPTP Limited'''（アムステルダム、ホラン）
    "あむすてるだむ",
    # あめりか /IPTP LLC/NO TOY GETS LEFT BEHIND/ベンジャミン/レコード・ワールド/一般的受容方式/
    "あめりか",
    "あらゆる",
    # ありがとう /ARIGATO!/有賀桃/謝謝你，在世界的角落找到我/謝謝你，在世界角落中找到我/
    "ありがとう",
    "ありし",
    "ありとあらゆる",
    "ある",
    # あるいは /テューキーの補題/ベン・ジョンソン/ホットスポット/
    "あるいは",
    "あれらの",
    "あんこーる",
    "あんな",
    # いいか /Then, for the thousands in attendance, and the millions watching at home./
    "いいか",
    "いかなる",
    "いとうすけのぶ",
    # いる /109万本/炒る/
    "いる",
    "いろんな",
    "いわゆる",
    "いんすとぅるめんたる",  # バンドのメンバー紹介項目
    "いんぜんたる",
    "いんでぃぺんでんとれーべる",  # バンドのメンバー紹介項目
    "いんでぃーず",  # バンドのメンバー紹介項目
    # うえいとれす /野村和子/
    "うえいとれす",
    # うち /86校/死者273人/死者・行方不明者約2万2000人/
    "うち",
    # えすか /擬餌状体/銀河刑務所の囚人を全員脱獄させる。/
    "えすか",
    # えっくす /400X/EX/○ごとX/
    "えっくす",
    "おかしな",
    "おそるべき",
    "おっきな",
    "おなじ",
    # おぷしょん /OPTION/作者情報/名前/
    "おぷしょん",
    "おもだった",
    "およそ",
    # および /UTF-32/江迎警察署 - 北部/相補誤差関数/
    "および",
    # おりじなる /TotheFarSeas -はるかな海へ-/原型/呪われた海/
    "おりじなる",
    # おりじなるからおけ /APlaceUndertheSun/BoomBoomMyHeart〈TVMIX〉/CHEERSFORYOU/Darlin'/GETLOVE/HERO/HERO（アカペラバージョン）/
    "おりじなるからおけ",
    "おるがん",  # バンドのメンバー紹介項目
    "おんなじ",
    "おんらいん",
    "おーいなる",
    "おーきな",
    "おーぷにんぐ",  # おーぷにんぐ /監督/
    "かかる",
    "かがやける",
    "かくぜんたる",
    "かくたる",
    "かっこたる",
    "かつ",
    # かまいたち /ひびきすぎ夫/伝令係・谷/森ガールの集い/
    "かまいたち",
    "からおけ",
    "かんさんたる",
    "かんぜんたる",
    "かんたる",
    "きぜんたる",
    "きたる",
    # きどうせんしがんだむてっけつのおるふぇんずげっこう /機動戦士ガンダム鉄血のオルフェンズ月鋼/
    "きどうせんしがんだむてっけつのおるふぇんずげっこう",
    # きどうせんしがんだむのとうじょうじんぶつじおんこうこくぐん /機動戦士ガンダムの登場人物ジオン公国軍/
    "きどうせんしがんだむのとうじょうじんぶつじおんこうこくぐん",
    # きどうせんしがんだむのとうじょうじんぶつちきゅうれんぽうぐん /機動戦士ガンダムの登場人物地球連邦軍/
    "きどうせんしがんだむのとうじょうじんぶつちきゅうれんぽうぐん",
    # きどうせんしがんだむのとうじょうじんぶつみんかんじん /機動戦士ガンダムの登場人物民間人/
    "きどうせんしがんだむのとうじょうじんぶつみんかんじん",
    # きゃっつ /CATS, Cats/
    "きゃっつ",
    # きょうのほんこん /今日の香港、明日の台湾、明後日の沖縄/
    "きょうのほんこん",
    # きょうのほんこんあすのたいわん /今日の香港、明日の台湾/
    "きょうのほんこんあすのたいわん",
    "きーぼーど",  # バンドのメンバー紹介項目
    # バンドのメンバー紹介項目を除外
    # ぎたー /8P/AYA/Aki/CAT/EBBY/EDDIE/GAK/GENTA/
    "ぎたー",
    "くしき",
    # ぐらびああいどる /寺口智香/愛心/
    "ぐらびああいどる",
    # アーティスト名が入ってきちゃうパターン
    # ぐりん /夏でSUKA?/
    "ぐりん",
    "げすと",  # バンドのメンバー紹介項目
    "げんぜんたる",
    # げーむぼーいからー /JリーグエキサイトステージGB/
    "げーむぼーいからー",
    # こっく /米沢誠/
    "こっく",
    # こっくえき /谷口駅/
    "こっくえき",
    "この",
    "これらの",
    # こんと /戦え!動物戦士ももいろアニマルZ 本編
    "こんと",
    "こんな",
    "こーした",
    "こーゆう",
    "こーりょーたる",
    "ごーごーたる",
    "さいたる",
    "さしたる",
    "さっくす",  # バンドのメンバー紹介項目
    "さっそーたる",
    "さつばつたる",
    "さらなる",
    "さる",
    # さん /ぴろし3/天井/
    "さん",
    # さんこみっくす /学生たちの道/
    "さんこみっくす",
    # さんばーすと /Gibson Les Paul Standard 1959 Historic Collection/
    "さんばーすと",
    "ざつぜんたる",
    "しかるべき",
    "しゃくぜんたる",
    "しゅたる",
    "しりーず",
    "しんしんたる",
    "せいせいどーどーたる",
    "せいぜんたる",
    "せいなる",
    "せつせつたる",
    "そういった",
    "そしらぬ",
    "そそたる",
    "その",
    "そぷらの",  # バンドのメンバー紹介項目
    "それらの",
    "そんな",
    "そーした",
    "そーぜんたる",
    "そーゆう",
    # 連体詞を除外(mecab-ipadic から抽出)
    # euc-grep 連体詞 Adnominal.csv | perl -pe 's/.*,//' | perl -MLingua::JA::Regular::Unicode=katakana2hiragana -nC -E 'chomp; push @a, katakana2hiragana($_); END { say join ",", map { qq!"$_"! } @a }'
    # かの、ある は除外している。
    "たいした",
    "たかだか",
    # ''CSS等の保護技術を回避してのDVDのリッピングは私的複製の対象外となり違法行為となる'''（ただし、CSS等の保護技術が使われていないDVDのリッピングについては、改正後も従来と変わりはない）
    "ただし",
    "ただならぬ",
    "たっての",
    "たの",
    "たんぜんたる",
    "たんたんたる",
    "たんなる",
    "だいそれた",
    # だぶるぜーたばーじょん Chai Maxx -ZZ ver.-,DNA狂詩曲 -ZZ ver.-,GOUNN -ZZ ver.-,MOON PRIDE -ZZ ver.-,Moon Revenge -ZZ ver.-,My Dear Fellow -ZZ ver.-,ZZ ver.,全力少女 -ZZ ver.-,月虹 -ZZ ver.-,白い風 -ZZ ver.-
    "だぶるぜーたばーじょん",
    "だんこたる",
    "だんぜんたる",
    "ちちたる",
    "ちっさな",
    "ちっちゃな",
    "ちょっとした",
    "ちょーぜんたる",
    "ちーさな",
    "てのーる",  # バンドのメンバー紹介項目
    "てれび",
    "とある",
    "とんだ",
    "とーの",
    "どの",
    "どらむ",  # バンドのメンバー紹介項目
    "どらむす",  # バンドのメンバー紹介項目
    "どんな",
    "どーどーたる",
    "どーゆう",
    "なき",
    "なだたる",
    "なんたる",
    "なんらかの",
    # 『'''NIU'''』（ニュ）は、[[日本]]の[[女性]][[歌手]]で、音楽グループ[[Every Little Thing]]のボーカリスト・[[持田香織]]が[[2010年]][[8月25日]]に発売した2枚目のソロ・[[アルバム]]である。
    "にゅ",
    "ばくぜんたる",
    "ばくたる",
    "ばす",  # バンドのメンバー紹介項目
    "ひょんな",
    "ひろいん",  # バンドのメンバー紹介項目
    "ひろびろたる",
    "びびたる",
    "ぴあの",  # バンドのメンバー紹介項目
    "ふとした",
    "ふんぜんたる",
    "ぷろぐらみんぐ",  # ぷろぐらみんぐ /望月英樹/
    "ぷろでゅーす",  # バンドのメンバー紹介項目
    "へいぜんたる",
    "べーす",  # バンドのメンバー紹介項目
    "べーすめんともんすたー",
    "ほんの",
    # ぼく /お姉さま/繆森/
    "ぼく",
    "ぼーかる",  # バンドのメンバー紹介項目
    # ぼーなすとらっく /AllYouMiss/AnswertoThisFlower/CircleofLife/DreamingStar/Ican'tfollowyou/KeepInThePockets[Remix]/
    "ぼーなすとらっく",
    "まさかの",
    # または /イルーニャ/インターラーケン修道院/カットアップ/
    "または",
    "まんぜんたる",
    # まーがれっとこみっくす /HEY☆坊や/こんにちはスザンヌ/幸福ゆきかしら?/愛がありますか?/手紙をください!/日の輪月の輪/
    "まーがれっとこみっくす",
    "みしらぬ",
    "もくもくたる",
    "もーもーたる",
    "ゆゆしき",
    "ゆーぜんたる",
    # らいぶ /Five Colours in Her Hair/LIVE/LiVE/L×I×V×E/Obviously/Room on 3rd Floor/That Girl/The Ballad of Paul K/Ultraviolet/耒部/雷舞/
    "らいぶ",
    # らゔ /LOVE/LOVE Seiko Matsuda 20th Anniversary Best Selection/LUV/Love/LØVE/♥♥♥LOVE♥♥♥/
    "らゔ",
    "りんれつたる",
    "れきぜんたる",
    "れっきとした",
    "ろくな",
    # '''FANZAアダルトアワード'''（ロゴ・{{lang-en-short|FANZA ADULT AWARD}}）
    "ろご",
    "わが",
    # ゑい /優勝内国産馬連合競走/長谷川榮/
    "ゑい",
    "ゔぃおら",  # バンドのメンバー紹介項目
    # わーむ /長虫/
    "わーむ",
    # ゔぇるんど /神器錬成/
    "ゔぇるんど",
    "ゔぉーかる",  # バンドのメンバー紹介項目
}


def read_filtered(fname):
    result = {}

    with open(fname, "r", encoding="utf-8") as ifh:
        for line in ifh:
            kanji, yomi = line.strip().split("\t")
            if yomi not in result:
                result[yomi] = []
            result[yomi].append(kanji)

    return result


def preproc(dic, skkdict):
    for y in IGNORE_YOMIS:
        dic.pop(y, None)

    # 読みが長音記号「ー」で始まるエントリを除外する
    for y in [k for k in dic if k.startswith("ー")]:
        dic.pop(y)

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
    with open(dictname, "w", encoding="utf-8") as ofp:
        # 東京スカイツリー,1288,1288,4569,名詞,固有名詞,一般,*,*,*,東京スカイツリー,トウキョウスカイツリー,トウキョウスカイツリー
        for yomi in sorted(dictionary.keys()):
            # ',' が入っているものがあると、CSV として壊れるので無視する
            if "," in yomi:
                continue

            for kanji in dictionary[yomi]:
                # ',' が入っているものがあると、CSV として壊れるので無視する
                if "," in kanji:
                    continue
                ofp.write(f"{kanji},1288,1288,{score},名詞,固有名詞,一般,*,*,*,{kanji},{yomi},{yomi}\n")


if __name__ == "__main__":
    import sys
    import time

    logging.basicConfig(level=logging.INFO)

    t0 = time.time()

    skkdicts = [parse_skkdict(path, encoding="euc-jp") for path in sys.argv[1:]]
    skkdict = merge_skkdict(skkdicts)

    result = read_filtered("dat/post_validated.tsv")
    result = preproc(result, skkdict)
    write_skkdict("SKK-JISYO.jawiki", result)
    write_mecabdic("mecab-userdic.csv", result)

    logging.info("Scanned: {0} seconds".format(time.time() - t0))
