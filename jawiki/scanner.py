import re

YOMI_PATTERN  = re.compile(r"""'''(.+?)'''（(.+?)）""")

def scan_words(s):
    while len(s) > 0:
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


