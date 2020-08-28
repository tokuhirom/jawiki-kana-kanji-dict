import pytest
from jawiki import skkdict

d = skkdict.parse_skkdict('SKK-JISYO.jawiki', encoding='utf-8')


@pytest.mark.parametrize("yomi", [
    ('きんぐぬー'),
    ('れいわ'),
    ('うちだかおる'),
    ('さかもとふじえ'),
    ('あかとりい'),
    ('いせきしこく'),
    ('きうちきょう'),
    ('おおとにー'),
    ('いんだらじゃえいげんまりゅう'),
    ('こちらかつしかくかめありこうえんまえはしゅつじょ'),
])
def test_yomo(yomi):
    assert yomi in d


@pytest.mark.parametrize("kanji,yomi", [
    ('安蘇山', 'あそさん'),
    ('あに。', 'あにまる'),
    ('南夕子', 'みなみゆうこ'),
    ('青井惟董', 'あおいこれただ'),
    ('赤プル', 'あかぷる'),
    ('安藤孝子', 'あんどうたかこ'),
    ('EX大衆', 'いーえっくすたいしゅう'),
    ('古崤関', 'ここうかん'),
    ('鬼滅の刃', 'きめつのやいば'),
    ('鬱多羅僧', 'うったらそう'),
    ('三衣一鉢', 'さんねいっぱつ'),
    ('中川幸永', 'なかがわゆきえ'),
    ('姶良サティ', 'あいらさてぃ'),
    ('青木十良', 'あおきじゅうろう'),
    ('穴門みかん', 'あなとみかん'),
])
def test_pair(kanji, yomi):
    print([kanji, yomi, d.get(yomi)])
    assert kanji in d.get(yomi)


@pytest.mark.parametrize("kanji,yomi", [
    # '''（初代）京山 華千代'''（きょうやま はなちよ、[[1904年]]（[[明治]]37年）[[8月11日]] - [[1983年]]（[[昭和]]58年）[[1月7日]]）
    # ('京山華千代' ,'きょうやまはなちよ'),
    ('お姉さま', 'ぼく'),
    ('109万本', 'いる'),
    ('擬餌状体', 'えすか'),
    ('銀河刑務所の囚人を全員脱獄させる。', 'えすか'),
    ('監督', 'あばんたいとる'),
    ('10代式守与太夫', 'しきもりよだゆう'),
    ('1703年の北アメリカ北東岸の襲撃', 'きたあめりかほくとうがんのしゅうげき'),
    ('島ぜんぶでおーきな祭', 'さい'),
    ('アジャリス', 'さんてぃあーご'),
    ('UTF-32', 'および'),
    ('江迎警察署 - 北部', 'および'),
    ('相補誤差関数', 'および'),
    ('二人で旅に出る理由は？', 'あいりす'),
    ('大切な者との記憶', 'きゅーぶ'),
    ('死者・行方不明者約2万2000人', 'うち'),
    ('死者273人', 'うち'),
    ('86校', 'うち'),
    ('INDIES', 'いんでぃーず'),
    ('ZAZZY', 'いんでぃーず'),
    ('長谷川榮', 'ゑい'),
    ('謝謝你，在世界的角落找到我', 'ありがとう'),
    ('謝謝你，在世界角落中找到我', 'ありがとう'),
    ('Five Colours in Her Hair', 'らいぶ'),
    ('LOVE Seiko Matsuda 20th Anniversary Best Selection', 'らゔ'),
    ('You♡I -Sweet Tuned by 5pb.-', 'ゆい'),
])
def test_no_pair(kanji, yomi):
    assert yomi not in d or kanji not in d.get(yomi)

# はいっていてはいけないもの
@pytest.mark.parametrize("yomi", [
    ('いずれもろっくふぃるだむ'),
    ('のちの'),
    ('あーけーどすてぃっく'),
    ('ぐらびああいどる'),
    ('いわゆる'),
    ('ぼーこーどあるいはぼどーこーど'),
    ('さんばーすと'),
    ('いいか'),
])
def test_not_in(yomi):
    assert yomi not in d

# INFO:root:めりー -> ['MELLIE', 'Mery', '個人所有', '尾道市土生幼稚園', '源清田小学校', '石岡市愛友幼稚園', '神戸市千鳥幼稚園', '秋田市土崎幼稚園', '郡山婦人会幼児保育所']                    
# INFO:root:べーすめんともんすたー -> ['BASEMENT MONSTAR', 'IMPACT.11×DFC', 'IMPACT.12×DFC', 'IMPACT.3', 'IMPACT.4', '激突3&IMPACT.9']                                                          
# INFO:root:てれび -> ['CVY自主放送', 'テレビ東京20年史', 'テレビ東京25年史', 'テレビ東京30年史', 'テレビ西日本', '見て']                                                                       
# INFO:root:しん -> ['Guitar：Shin', 'SHIN', 'SIN', 'SINN', 'Shin', 'Shing', 'Sin']                                                                                                             
# INFO:root:さんきゅー -> ['THANK YOU', 'Thank You', 'Thank You!', 'Thank you', 'Thank you, ROCK BANDS! 〜UNISON SQUARE GARDEN 15th Anniversary Tribute Album〜', 'thank you.']                 
# INFO:root:かつ -> ['KAT', 'KATSU', 'KATSU!', 'KATZ', 'Katsu', '日本初']                                                                                                                       







