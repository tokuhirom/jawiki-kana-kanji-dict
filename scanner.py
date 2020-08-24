import re

TITLE_PATTERN = re.compile(r'''.*<title>(.+)</title>''')
YOMI_PATTERN  = re.compile(r"""'''(.+?)'''（(.+?)）""")

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

                if not ignorable:
                    p = re.findall(YOMI_PATTERN, line)
                    if p:
                        for n in p:
                            yield (title, n[0], n[1])


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
if __name__=='__main__':
    import sys
    import time

    for fname in sys.argv[1:]:
        print("Scanning " + fname)
        t0 = time.time()

        scanner = WikipediaXmlScanner()

        with open('scanned.tsv', 'w', encoding='utf-8') as ofh:
            for element in scanner.scan(fname):
                ofh.write("%s\t%s\t%s\n" % (
                    element[0].replace("\t", " "),
                    element[1].replace("\t", " "),
                    element[2].replace("\t", " ")
                ))

        print("Scanned: " + fname + " in " + str(time.time()-t0) + " seconds")

