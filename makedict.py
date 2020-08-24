import re

# filter.py 機械的にはとりのぞきにくいエントリを、このフェーズで除外。
#
# あふがにすたんふんそう /アフガニスタン紛争（2001年-現在）/1979年-1989年のアフガニスタン紛争/アフガニスタン紛争/
# '''伊東彦兵衛尉藤原祐信（すけのぶ）伊東 祐信'''（いとう すけのぶ）は、[[室町時代]]の武士。
#
IGNORE_ENTRIES = set(
    ['あふがにすたんふんそう',
    'いとうすけのぶ'
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

#   for my $yomi (sort keys %dict) {
#       # 特殊記号始まりの読みになっているものを除外する
#       next if $yomi =~ /^[〜『「〈《]/;

#       my @kanji = grep { ! $skkdict->{$yomi}{$_} } uniq @{$dict{$yomi}};
#       next unless @kanji;
#       printf {$ofh} "%s /%s/\n", $yomi, join('/', @kanji);
#   }
    print("Scanned: " + str(time.time()-t0) + " seconds")

