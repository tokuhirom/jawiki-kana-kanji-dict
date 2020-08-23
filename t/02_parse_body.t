use strict;
use warnings;
use utf8;

use Test::Base::Less;
use Test::More;
use Test::More::UTF8;
use YAML;

use W;

binmode( STDOUT, ":utf8" );
binmode( STDERR, ":utf8" );

filters {
    expected => [qw/eval/],
};

for my $block (blocks) {
    my $got = W::parse_body($block->input);
    note Dump($got, $block->expected);
    is_deeply($got, $block->expected);
}

done_testing;
     
__DATA__
     
===
--- input
'''福原 元{{CP932フォント|僴}}'''（ふくばら もとたけ）
--- expected
[
    ['福原元僴', 'ふくばらもとたけ'],
]

===
--- input
'''[[瘀血]]証'''（おけつしょう）
--- expected
[
    ['瘀血証', 'おけつしょう'],
]

===
--- input
'''司馬 {{JIS2004フォント|遼󠄁}}太郎'''（しば りょうたろう、[[1923年]]（[[大正]]12年）[[8月7日]] - [[1996年]]（[[平成]]8年）[[2月12日]]）は、日本の[[小説家]]、[[ノンフィクション作家]]、[[評論家]]。本名、'''福田 定一'''（ふくだ ていいち）。筆名の由来は「'''[[司馬遷]]'''に'''遼'''（はるか）に及ばざる日本の者（故に'''太郎'''）」から来ている。!
--- expected
[
    ['司馬遼󠄁太郎','しばりょうたろう'],
    ['福田定一', 'ふくだていいち'],
],


===
--- input
'''路面電車'''（ろめんでんしゃ&lt;!--、Tram、Tramway、Streetcar、{{lang-de-short|Straßenbahn}}--&gt;）は、主に[[道路]]上に敷設された[[軌道 (鉄道)|軌道]]（[[併用軌道]]）を用いる「路面鉄道」（{{lang-en-short|Tram}}、Tramway、Streetcar、{{lang-de-short|Straßenbahn}}）を走行する[[電車]]である。類似のシステムに[[ライトレール|ライト・レール・トランジット]]、[[トラムトレイン]]、[[ゴムタイヤトラム]]なども存在する。
--- expected
[
    ['路面電車', 'ろめんでんしゃ']
]

===
--- input
'''津田 雅美'''（つだ まさみ、[[1970年]][[7月9日]]<ref name="profile">{{Cite web|url=http://www.hakusensha.co.jp/artist/profile.php?artistname=%92%C3%93c%89%EB%94%FC&artistname2=%82%C2%82%BE%82%DC%82%B3%82%DD&keyword=%82%C2+%82%C3&home=%90_%93%DE%90%EC%8C%A7&birthday=7%8C%8E9%93%FA&bloodtype=B%8C%5E&debut=1993%94N%81u%91%9D%8A%A7%83%89%83%89%83%7E%83X%83e%83%8A%81%5B%83X%83y%83V%83%83%83%8B%81v%81w%89%EF%82%A6%82%C4%82%E6%82%A9%82%C1%82%BD%81x|title=白泉社 作家データベース 津田雅美|publisher=白泉社 |accessdate=2016-02-03}}</ref> - ）は、[[日本]]の[[漫画家]]。[[神奈川県]]出身<ref name="profile"/>。[[ABO式血液型|血液型]]はO型<ref name="6巻145"> {{Cite book|和書|author=津田雅美|year=2016|title=ヒノコ|page=145|volume=6巻|publisher=白泉社|isbn=978-4592211037}} </ref>{{efn|2016年以前のプロフィールではB型<ref name="profile"/>になっているが、病院で調べたところ、O型だったと訂正している<ref name="6巻145"/>}}。
--- expected
[ [ '津田雅美', 'つだまさみ' ] ]

===
--- input
'''士郎 正宗'''（しろう まさむね、[[1961年]][[11月23日]] - ）は、[[日本]]の[[漫画家]]、[[イラストレーター]]。
--- expected
[ [ '士郎正宗', 'しろうまさむね' ] ]

===
--- input
'''佐々木 倫子'''（ささき のりこ&lt;ref&gt;『花與夢雑誌』1993年9月10日号（第17期）、大然文化事業股份公司、P77,P232。&lt;/ref&gt;、[[1961年]][[10月7日]] - ）は、[[日本]]の[[漫画家]]。
--- expected
[ [ '佐々木倫子', 'ささきのりこ' ] ]

===
--- input
'''[[葉状体]]'''（ようじょうたい）とに分けられる。
--- expected
[ [ '葉状体', 'ようじょうたい' ] ]

===
--- input
** '''[[マイクロソフト]]'''（ただし、[[Xbox 360]]はどちらの規格にも対応せず、[[Microsoft Windows Vista]]は両規格に対応していた）
--- expected
[]

===
--- input
'''京浜急行電鉄株式会社'''（けいひんきゅうこうでんてつ、{{Lang-en-short|Keikyu Corporation}}）は、[[神奈川県]][[横浜市]]に本社を置く鉄道会社である。
--- expected
[[qw(京浜急行電鉄 けいひんきゅうこうでんてつ)]]

===
--- input
'''一般社団法人映画産業団体連合会'''（えいがさんぎょうだんたいれんごうかい）
--- expected
[[qw(映画産業団体連合会 えいがさんぎょうだんたいれんごうかい)]]

===
--- input
'''三信上市場[[停留所|停留場]]'''（さんしんかみいちばていりゅうじょう）
--- expected
[[qw/三信上市場停留場 さんしんかみいちばていりゅうじょう/]]

===
--- input
'''&amp;#39641;崎ひとみ'''（たかさきひとみ）
--- expected
[[qw/髙崎ひとみ たかさきひとみ/]]

