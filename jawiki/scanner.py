import re


def scan_until_closing_paren(s, start_level=1):
    level = start_level
    yomi = ''
    for i in range(len(s)):
        if s[i] == '（' or s[i] == '(':
            level += 1
        elif s[i] == '）' or s[i] == ')':
            level -= 1
            if level == 0:
                s = s[i+1:]
                return s, yomi
        yomi += s[i]

    # 最後まで対応するコッカが見つからない場合でも、返す。
    return s, yomi

# {{読み仮名|'''漢字'''|かな}} のパターンを除去する
# （='''糞掃'''）
# '''漢字'''（ふりがな）
# 『'''漢字'''』（ふりがな）
# 『'''EX大衆'''（イーエックスたいしゅう）』
YOMI_PATTERN  = re.compile(r"""\{\{読み仮名\|'''(.+?)'''\|([^|]+?)\|?\}\}|'''([^']+)'''[^（』]|'''(.+?)'''（(.+?)(?:[）\)]|$)|『'''(.+?)'''』?（(.+?)(?:[）\)]|$)""")

def scan_words(s):
    while True:
        m = YOMI_PATTERN.search(s)
        if m:
            # {{読み仮名|'''漢字'''|かな}}
            if m[1] and m[2]:
                yield m[1], m[2]
                s = s[m.end():]
                continue

            # （='''糞掃'''）
            if m[3]:
                s = s[m.end():]
                continue

            # '''漢字'''（ふりがな）
            for i, j in [(4,5), (6,7)]:
                if m[i] and m[j]:
                    kanji = m[i]
                    yomi = m[j]
                    if '（' in yomi:
                        s = s[m.end():]
                        s, ext_yomi = scan_until_closing_paren(s, start_level=yomi.count('（')+0)
                        yomi += '）' + ext_yomi
                    else:
                        s = s[m.end():]
                    yield kanji, yomi
                    break

            continue

        break

