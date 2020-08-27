import re

YOMI_PATTERN  = re.compile(r"""'''(.+?)'''（(.+?)）""")

def scan_until_closing_paren(s):
    level = 1
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

# '''漢字'''（ふりがな）
# 『'''漢字'''』（ふりがな）
START_PATTERN = re.compile(r"(『?''')")
def scan_pattern1(s):
    m = START_PATTERN.search(s)
    if m is None:
        return s, None, None

    end_token = r"'''（" if m[0] == "'''" else "'''』（"

    end_start = s.find(end_token, len(m[0]))
    if end_start!=-1:
        kanji = s[m.end():end_start]
        s = s[end_start+len(end_token):]
        s, yomi = scan_until_closing_paren(s)
        return s, kanji, yomi

    return s, None, None

def scan_pattern(start_token, end_token):
    def scan_pattern2(s, start_token="'''", end_token="'''（"):
        m = s.find(start_token)
        if m==-1:
            return s, None, None

        end_start = s.find(end_token, m)
        if end_start!=-1:
            kanji = s[m+len(start_token):end_start]
            s = s[end_start+len(end_token):]
            s, yomi = scan_until_closing_paren(s)
            return s, kanji, yomi

        return s, None, None
    return lambda s: scan_pattern2(s, start_token, end_token)


# {{読み仮名|'''プラカシー油'''|ぷらかしーゆ}}
def scan_yomigana(s):
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
    if yomi[-1] == '|':
        yomi = yomi[:-1]

    s = s[r+2:]

    return s, kanji, yomi

def scan_words(s):
    for scanner in [scan_yomigana]:
        t = s
        while True:
            t, kanji, yomi = scanner(t)
            if kanji != None:
                yield kanji, yomi
            else:
                break

    # {{読み仮名|'''漢字'''|かな}} のパターンを除去する
    s = re.sub(r"""\{\{読み仮名\|'''.*?'''\|.*?\|?\}\}""", '', s)
    for scanner in [scan_pattern("'''", "'''（"), scan_pattern("『'''", "'''』（")]:
        t = s
        while True:
            t, kanji, yomi = scanner(t)
            if kanji != None:
                yield kanji, yomi
            else:
                break

