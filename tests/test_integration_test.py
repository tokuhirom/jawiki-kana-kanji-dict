import pytest
from jawiki.converter import Converter
from jawiki.pre_validate import PreValidator
from jawiki.post_validate import PostValidator
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")
converter = Converter()
pre_validator = PreValidator()
post_validator = PostValidator(tokenizer)

testdata = []
with open('tests/mapping.tsv', 'r') as fp:
    for line in fp:
        m = line.strip().split("\t")
        if len(m) == 3:
            m.append(None)
            m.append(None)
        if len(m) > 1:
            testdata.append(m)


def process(title, kanji, yomi):
    if not pre_validator.validate(title, kanji, yomi):
        return
    kanji, yomi = converter.convert(kanji, yomi)
    if not post_validator.post_validate(kanji, yomi):
        return kanji, yomi


@pytest.mark.parametrize("input_title,input_kana,input_yomi,expected_kanji,expected_yomi", testdata)
def test_tsv(input_title, input_kana, input_yomi, expected_kanji, expected_yomi):
    m = process(input_title, input_kana, input_yomi)
    if m:
        got_kanji, got_yomi = m
        assert got_kanji == expected_kanji and got_yomi == expected_yomi
    else:
        assert not expected_yomi and not expected_kanji
