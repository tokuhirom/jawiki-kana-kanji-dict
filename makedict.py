import re

# filter.py で機械的にはとりのぞきにくいエントリを、このフェーズで除外。
IGNORE_ENTRIES = set(
    [
        'あふがにすたんふんそう',
        'いとうすけのぶ',
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

def parse_skkdict(path):
    result = {}

    with open(skkdictpath, 'r', encoding='euc-jp') as fp:
        for line in fp:
            if line.startswith(';;'):
                continue

            m = line.strip().split(' ', 1)
            yomi, kanjis = m
            kanjis = kanjis.lstrip('/').rstrip('/').split('/')
            kanjis = [re.sub(';.*', '', k) for k in kanjis]

            result[yomi] = set(kanjis)

    return result

if __name__=='__main__':
    import sys
    import time

    t0 = time.time()

    result = {}

    skkdictpath = sys.argv[1]

    skkdict = parse_skkdict(skkdictpath)

    with open('filtered.tsv', 'r', encoding='utf-8') as ifh, \
        open('SKK-JISYO.jawiki', 'w', encoding='utf-8') as ofh:
        for line in ifh:
            kanji, yomi = line.strip().split("\t")
            if yomi not in result:
                result[yomi] = []
            result[yomi].append(kanji)

        for yomi in sorted(result.keys()):
            if yomi in IGNORE_ENTRIES:
                continue

            kanjis = [x for x in sorted(set(result[yomi])) if yomi not in skkdict or x not in skkdict[yomi]]
            if len(kanjis) != 0:
                ofh.write("%s /%s/\n" % (yomi, '/'.join(kanjis)))
            if len(kanjis) > 10:
                print("%s -> %s" % (yomi, kanjis))

    print("Scanned: " + str(time.time()-t0) + " seconds")

