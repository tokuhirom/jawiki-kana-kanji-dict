from jawiki import skkdict

d = skkdict.parse_skkdict('SKK-JISYO.jawiki', encoding='utf-8')

assert 'きんぐぬー' in d
assert 'れいわ' in d
assert 'きめつのやいば' in d
assert 'うちだかおる' in d
assert 'さかもとふじえ' in d
assert 'あかとりい' in d
assert 'いせきしこく' in d
assert 'きうちきょう' in d


assert 'いずれもろっくふぃるだむ' not in d
assert 'のちの' not in d
assert 'あーけーどすてぃっく' not in d
assert 'ぐらびああいどる' not in d

