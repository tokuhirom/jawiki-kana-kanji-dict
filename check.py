from jawiki import skkdict

d = skkdict.parse_skkdict('SKK-JISYO.jawiki', encoding='utf-8')

assert 'きんぐぬー' in d
assert 'れいわ' in d
assert 'うちだかおる' in d
assert 'さかもとふじえ' in d
assert 'あかとりい' in d
assert 'いせきしこく' in d
assert 'きうちきょう' in d
assert 'おおとにー' in d
assert 'いんだらじゃえいげんまりゅう' in d
assert 'こちらかつしかくかめありこうえんまえはしゅつじょ' in d

assert '安蘇山' in d.get('あそさん')
assert 'あに。' in d.get('あにまる')
assert 'お姉さま' not in d.get('ぼく')
assert '南夕子' in d.get('みなみゆうこ')
assert '青井惟董' in d.get('あおいこれただ')
assert '赤プル' in d.get('あかぷる')
assert '安藤孝子' in d.get('あんどうたかこ')
assert 'EX大衆' in d.get('いーえっくすたいしゅう')
assert '京山華千代' in d.get('きょうやまはなちよ')
assert '古崤関' in d.get('ここうかん')

assert '109万本' not in d.get('いる')

assert 'いずれもろっくふぃるだむ' not in d
assert 'のちの' not in d
assert 'あーけーどすてぃっく' not in d
assert 'ぐらびああいどる' not in d
assert 'いわゆる' not in d

# -うったらそう /鬱多羅僧/
# -さんねいっぱつ /三衣一鉢/
# -なかがわゆきえ /中川幸永/




# assert 'きめつのやいば' in d
