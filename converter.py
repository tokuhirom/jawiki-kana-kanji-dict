from jawiki import converter
from jawiki.file_processor import FileProcessor


def converter_worker(chunk):
    jawiki_converter = converter.Converter()
    results = []
    for line in chunk:
        splitted = line.strip().split("\t")
        if len(splitted) != 3:
            continue
        title, kanji, yomi = splitted
        kanji, yomi = jawiki_converter.convert(kanji, yomi)
        if len(yomi) > 0:
            results.append([kanji, yomi])
    return results


if __name__ == '__main__':
    with open('dat/converted.tsv', 'w', encoding='utf-8') as ofh:
        def converter_writer(result):
            kanji, yomi = result
            ofh.write(f"{kanji}\t{yomi}\n")


        file_processor = FileProcessor()
        file_processor.run(
            'dat/pre_validated.tsv', converter_worker,
            converter_writer
        )
