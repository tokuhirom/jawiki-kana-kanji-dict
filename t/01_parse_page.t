use strict;
use warnings;
use utf8;

use Test::Base::Less;
use Test::More;
use YAML;
use Test2::Plugin::UTF8;

use W;

binmode( STDOUT, ":utf8" );
binmode( STDERR, ":utf8" );

filters {
    expected => [qw/eval/],
};

for my $block (blocks) {
    my $got = W::parse_page($block->input);
    note Dump($got, $block->expected);
    is_deeply($got, $block->expected);
}

done_testing;
     
__DATA__

===
--- input
<title>Intel 4004</title>
<text>
'''4004'''（よんまるまるよん、と読まれることが多い）は、[[アメリカ合衆国|米国]][[インテル|インテル社]]によって開発された1チップの[[マイクロプロセッサ]]であり、軍用の[[セントラル・エア・デー タ・コンピュータ|MP944]]&lt;ref&gt;[[F-14 (戦闘機)|F-14戦闘機]]用[[セントラル・エア・データ・コンピュータ|Central Air Data Computer]]&lt;/ref&gt;、組み込み用のTI製[[TMS-1000]]等とほぼ同時期 の、世界最初期のマイクロプロセッサのひとつである。周辺ファミリ[[集積回路|IC]]を含めてMCS-4 Micro Computer Set、あるいは略し単にMCS-4とも呼ぶ。
</text>
--- expected
[ ]

===
--- input
<title>w3m</title>
<text>
'''w3m'''（ダブリューサンエム または ダブリュースリーエム）は
</text>
--- expected
[
]

===
--- input
<title>三科</title>
<text>
:* '''{{linktext|六根}}'''（ろっこん、{{lang-sa-short|ṣaḍ-indriya}}） - 主観の側の六種の器官{{sfn|櫻部・上山|2006|p=60}}、感官{{sfn|村上|2010|p=233}}のこと。'''{{linktext|六内入処}}'''（ろくないにゅうしょ）とも。
</text>
--- expected
[
    ['三科', '六根', 'ろっこん'],
    ['三科', '六内入処', 'ろくないにゅうしょ'],
]

===
--- input
<title>少年画報社</title>
<text>
'''株式会社少年画報社'''（しょうねんがほうしゃ、英語表記：Shonen-gahosha Co., Ltd.）は、主に[[漫画]]を出版している[[日本]]の[[出版社]]。
</text>
--- expected
[
    ['少年画報社', '少年画報社', 'しょうねんがほうしゃ'],
]

===
--- input
  <page>
    <title>綾瀬川 (四股名)</title>
    <ns>0</ns>
    <id>3128474</id>
    <revision>
      <id>54252999</id>
      <timestamp>2015-01-28T06:00:29Z</timestamp>
      <contributor>
        <username>まっきんりい</username>
        <id>787822</id>
      </contributor>
      <comment>[[WP:AES|←]]新しいページ: ''''綾瀬川'''（あやせがわ）は、以下の[[力士]]。  *[[綾瀬川山左エ門]] - 最高位[[大関]]。 *[[綾瀬川山左エ門 (1876年生)]] -...'</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text bytes="383" xml:space="preserve">'''綾瀬川'''（あやせがわ）は、以下の[[力士]]。

*[[綾瀬川山左エ門]] - 最高位[[大関]]。
*[[綾瀬川山左エ門 (1876年生)]] - 最高位[[関脇]]。
*[[綾瀬川三左エ門]] - 最高位[[前頭]]5枚目。

いずれも、元は[[大坂相撲]]に所属した力士。

{{デフォルトソート:あやせかわ}}
{{aimai}}
[[Category:四股名]]</text>
      <sha1>01324wx6u0y7sjlycuqu2hoqvol60z2</sha1>
    </revision>
  </page>
--- expected
[
    ['綾瀬川 (四股名)', '綾瀬川', 'あやせがわ'],
]


===
--- input
<title>中央州</title>
<text>
'''Keyboard / kAoru ikArAshi / 五十嵐 馨'''（いからし かおる）
</text>
--- expected
[]
