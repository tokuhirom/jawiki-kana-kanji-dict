from janome.tokenizer import Tokenizer

from jawiki.file_processor import FileProcessor
from jawiki.post_validate import PostValidator

tokenizer = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")

post_validator = PostValidator(tokenizer)


def worker(chunk):
    results = []
    for line in chunk:
        splitted = line.strip().split("\t")
        if len(splitted) != 2:
            continue
        kanji, yomi = splitted
        skip_reason = post_validator.post_validate(kanji, yomi)
        results.append([kanji, yomi, skip_reason])
    return results


if __name__ == '__main__':
    with open('logs/skipped.log', 'w', encoding='utf-8') as skipfp, \
            open('dat/post_validated.tsv', 'w', encoding='utf-8') as wfp:
        def writer(result):
            kanji, yomi, skip_reason = result
            if skip_reason:
                skipfp.write(f"{skip_reason}\t{kanji}\t{yomi}\n")
            else:
                wfp.write(f"{kanji}\t{yomi}\n")


        file_processor = FileProcessor()
        file_processor.run(
            'dat/converted.tsv', worker,
            writer
        )
