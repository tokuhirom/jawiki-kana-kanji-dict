import re
from jawiki.skkdict import merge_skkdict, parse_skkdict

# filter.py で機械的にはとりのぞきにくいエントリを、このフェーズで除外。
IGNORE_ENTRIES = set(
    [
        'あふがにすたんふんそう',
        'いとうすけのぶ',
        # あめりか /IPTP LLC/NO TOY GETS LEFT BEHIND/ベンジャミン/レコード・ワールド/一般的受容方式/
        'あめりか',
        # さん /ぴろし3/天井/
        'さん',
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
    # remove entries in skk dict.
    for yomi in sorted(dic.keys()):
        dic[yomi] = [kanji for kanji in sorted(set(dic[yomi])) if not should_skip(kanji, yomi, skkdict)]

    return dic


def should_skip(kanji, yomi, skkdict):
    if yomi not in skkdict:
        return False

    if kanji in skkdict[yomi]:
        return True

    # おめが /冥王計画ゼオライマーΩ/闘神都市Ω/
    # のようなケースを除外する
    for skk_kanji in skkdict[yomi]:
        if skk_kanji in kanji and skk_kanji != kanji:
            if yomi.startswith('あいおい'):
                print("skipped: yomi=%s skk_kanji=%s kanji=%s" % (yomi, skk_kanji, kanji))
            return True

    return False

if __name__=='__main__':
    import sys
    import time

    t0 = time.time()

    skkdictpath = sys.argv[1]

    skkdicts = [parse_skkdict(path, encoding='euc-jp') for path in sys.argv[1:]]
    skkdict = merge_skkdict(skkdicts)

    result = read_filtered('filtered.tsv')
    result = preproc(result, skkdict)

    with open('SKK-JISYO.jawiki', 'w', encoding='utf-8') as ofh:
        for yomi in sorted(result.keys()):
            if yomi in IGNORE_ENTRIES:
                continue

            kanjis = result[yomi]
            if len(kanjis) != 0:
                ofh.write("%s /%s/\n" % (yomi, '/'.join(kanjis)))
            if len(kanjis) > 20:
                print("%s -> %s" % (yomi, kanjis))

    print("Scanned: " + str(time.time()-t0) + " seconds")

