from jawiki import skkdict

d = skkdict.parse_skkdict('SKK-JISYO.jawiki', encoding='utf-8')

assert 'きんぐぬー' in d
assert 'れいわ' in d
assert 'いずれもろっくふぃるだむ' not in d
assert 'のちの' not in d

