from jawiki import filter as jawiki_filter

from janome.tokenizer import Tokenizer


class Container:
    def __init__(self):
        self.tokenizer = None
        self.filter = None

    def get_tokenizer(self):
        if not self.tokenizer:
            self.tokenizer = Tokenizer()
        return self.tokenizer

    def get_filter(self):
        if not self.filter:
            skipfh = open('skipped.tsv', 'w', encoding='utf-8')

            def skip_logger(reason, line):
                skipfh.write("%s\t%s\n" % (reason.replace("\t", ' '), str(line).replace("\t", ' ')))

            self.filter = jawiki_filter.WikipediaFilter(skip_logger, tokenizer=self.get_tokenizer())

        return self.filter
