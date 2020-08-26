import re

YOMI_PATTERN  = re.compile(r"""'''(.+?)'''（(.+?)）""")

def scan_words(s):
    while len(s) > 0:
        s, kanji, yomi = scan_yomigana(s)
        if kanji != None:
            yield (kanji, yomi)
            continue

        n = s.find(r"'''")
        if n==-1:
            break
        m = s.find(r"'''（", n+3)
        if m==-1:
            break

        kanji = s[n+3:m]
        s = s[m+len("'''（"):]

        level = 1
        yomi = ''
        for i in range(len(s)):
            if s[i] == '（' or s[i] == '(':
                level += 1
            elif s[i] == '）' or s[i] == ')':
                level -= 1
                if level == 0:
                    s = s[i+1:]
                    yield (kanji, yomi)
                    break
            yomi += s[i]

        # 最後まで対応するコッカが見つからない
        if level != 0:
            s = ''
            yield (kanji, yomi)

def scan_yomigana(s):
    # {{読み仮名|'''プラカシー油'''|ぷらかしーゆ}}
    p = s.find(r"{{読み仮名|'''")
    if p==-1:
        return s, None, None

    q = s.find(r"'''|", p+len("{{読み仮名|'''"))
    if q==-1:
        return s, None, None

    kanji = s[p+len("{{読み仮名|'''"):q]

    r = s.find(r"}}", q+4)
    if r==-1:
        return s, None, None

    yomi = s[q+4:r]

    s = s[r+2:]

    return s, kanji, yomi

