import re

from jawiki import scanner

TITLE_PATTERN = re.compile(r'''.*<title>(.+)</title>''')


class WikipediaXmlScanner:
    def scan(self, filename):
        title = None
        ignorable = False

        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                m = TITLE_PATTERN.match(line)
                if m:
                    title = m[1]
                    ignorable = self.is_ignorable_title(title)

                if '<comment>' in line:
                    # skip comment line.
                    continue

                # :: '''二人で旅に出る理由は？'''（アイリス（[[悠木碧]]・[[茅野愛衣]]）） - 作曲 / 編曲：山本真央樹・北川勝利
                if '作曲 / 編曲' in line:
                    continue

                if not ignorable:
                    for m in scanner.scan_words(line):
                        if title == '令和':
                            print(title, m[0], m[1])
                        yield (title, m[0], m[1])

    def is_ignorable_title(self, title):
        if title == '常用漢字':
            return True

        for prefix in ('Wikipedia:', 'MediaWiki:', 'Template:', 'モジュール:', 'Portal:'):
            if title.startswith(prefix):
                return True

        # '国の一覧', 'ゲーム会社一覧', etc.
        for suffix in ('一覧'):
            if title.endswith(suffix):
                return True

        if '曖昧さ回避' in title:
            return True

        return False


# around 3 minutes on my SSD.
if __name__ == '__main__':
    import time

    fname = 'dat/grepped.txt'
    print(f"Scanning {fname}")
    t0 = time.time()

    wikipedia_scanner = WikipediaXmlScanner()

    with open('dat/scanned.tsv', 'w', encoding='utf-8') as ofh:
        for element in wikipedia_scanner.scan(fname):
            ofh.write("%s\t%s\t%s\n" % (
                element[0].replace("\t", " "),
                element[1].replace("\t", " "),
                element[2].replace("\t", " ")
            ))

    print(f"Scanned: {fname} in {str(time.time() - t0)} seconds")
