package W;
use strict;
use warnings;
use utf8;
use 5.010_001;

use Lingua::JA::Regular::Unicode qw/katakana2hiragana/;
use Term::ANSIColor;
use HTML::Entities qw/decode_entities/;

sub debug {
    print "$_[0]\n" if $ENV{DEBUG};
}

sub parse_title {
    my $page = shift;

    $page =~ m!<title>(.*?)</title>!;
    return $1;
}


sub parse_body {
    my $page = shift;

    if ($page =~ m{<text[^>]*>(.*)</text>}s) {
        return parse_text($1);
    } else {
        die "Missing text part: $page";
    }
}

sub parse_text {
    my $text_part = shift;

    my @results;

    while ($text_part =~ s/'''(.+?)'''（(.+?)）//) {
        my $kanji = $1;
        my $yomi  = $2;

        for (\$kanji, \$yomi) {
            $$_ =~ s!&lt;ref.*?&gt;.*?&lt;/ref&gt;!!g; # &lt;ref&gt;1883(明治)年宣下、明治天皇&lt;/ref&gt;
            $$_ =~ s!&lt;ref&gt;.*!!g; # unmatched <ref> tag(maybe broken parsing in this tool)
            $$_ =~ s/\{\{lang-en-short\|.+?\}\}//g;
            $$_ =~ s/\{\{lang-en\|.+?\}\}//g;
            $$_ =~ s/&lt;!--.*--&gt;//g;
            $$_ =~ s/\{\{lang\|[a-zA-Z_-]+\|(.+?)\}\}/$1/g; # {{lang|en|AMBAC}}
            $$_ =~ s/\{\{JIS2004フォント\|(.+)\}\}/$1/g; # '''司馬 {{JIS2004フォント|遼󠄁}}太郎'''
            $$_ =~ s/\{\{linktext\|(.+)\}\}/$1/g; # '''{{linktext|六根}}'''（ろっこん）
            $$_ =~ s/\{\{CP932フォント\|(.+)\}\}/$1/g; # {{CP932フォント|髙}}千代酒造
            $$_ =~ s/\{\{Anchor\|(.+)\}\}/$1/g; # {{Anchor|穴子包丁}}
        }

        # [[ページ名|リンクラベル]] 
        $kanji =~ s!\[\[(.*)\|(.*)\]\]!$2!g;

        # '''[[葉状体]]'''（ようじょうたい）
        # '''[[瘀血]]証'''（おけつしょう）
        $kanji =~ s!\[\[(.*)\]\]!$1!g;

        # よみがないものは除外。
        if (length($yomi) == 0) {
            debug("NO YOMI");
            next;
        }
        # よみがカタカナオンリーのものはなくす
        next if $yomi =~ /^[ア-ン・]+$/;
        # 平仮名を含んでないエントリをスキップする
        next unless $yomi =~ /[あ-ん]/;

        # '''[[マイクロソフト]]'''（ただし、[[Xbox 360]]はどちらの規格にも対応せず、[[Microsoft Windows Vista]]は両規格に対応していた）
        if ($yomi =~ /^ただし、/) {
            next;
        }
        # この音は'''ハーフ・ストップ'''（あるいはエコー、ハーフ・ミュート）と呼ばれる。
        if ($yomi =~ /^あるいは/) {
            next;
        }

        # ''w3m'''（ダブリューサンエム または ダブリュースリーエム）
        # このケースは、両方登録しなくていいのではないか。
        if ($yomi =~ / または /) {
            next;
        }

        # 、 以後は除去
        $yomi =~ s/、.*//;

        # 空白除去
        $kanji =~ s/ //g;
        $kanji =~ s/　//g;
        $yomi =~ s/ //g;

        if ($kanji =~ /'''/) {
            debug("Skip: contains q/'''/");
            next;
        }

        # 株式会社少年画報社:しょうねんがほうしゃ -> 少年画報社:しょうねんがほうしゃ
        # 京浜急行電鉄株式会社:けいひんきゅうこうでんてつ -> 京浜急行電鉄:けいひんきゅうこうでんてつ
        for my $type (
            [qw/株式会社 かぶしきがいしゃ/],
            [qw/一般社団法人 いっぱんしゃだんほうじん/],
            [qw/学校法人 がっこうほうじん/],
            [qw/公益財団法人 こうえきざいだんほうじん/],
            [qw/公益社団法人 こうえきしゃだんほうじん/],
            [qw/特定非営利活動法人 とくていひえいりかつどうほうじん/],
        ) {
            my ($k, $y) = @$type;
            if ($kanji =~ /^$k/ && $yomi !~ /^$y/) {
                $kanji =~ s/^$k//;
            }
            if ($kanji =~ /^$k/ && $yomi =~ /^$y/) {
                $kanji =~ s/^$k//;
                $yomi =~ s/^$y//;
            }
            if ($kanji =~ /$k$/ && $yomi !~ /$y$/) {
                $kanji =~ s/$k$//;
            }
            if ($kanji =~ /$k$/ && $yomi =~ /$y$/) {
                $kanji =~ s/$k$//;
                $yomi =~ s/$y$//;
            }
        }

        $kanji =~ s/(&amp;)/decode_entities $1/gei;
        $kanji =~ s/(&[a-z0-9_-]+;)/decode_entities $1/gei;
        $kanji =~ s/&#x([a-f0-9]+);/pack "U", hex($1)/gei;
        $kanji =~ s/&#(\d+);/pack "U", $1/ge;

        # '''池の平スノーパーク（旧白樺リゾートスキー場）'''（いけのたいらすのーぱーく）
        $kanji =~ s/（旧.*）//;

        debug("    CODE<<$kanji>> YOMI<<$yomi>> @{[ length($yomi) ]}\n");
        push @results, [$kanji, katakana2hiragana($yomi)];
    }
    return \@results;
}

sub parse_page {
    my $page = shift;
    my $skip_logger = shift // sub { };

    my $title = W::parse_title($page);
    for my $re (
        qr/一覧$/, # '国の一覧' or 'ゲーム会社一覧'
        qr/^Wikipedia:/,
        qr/^Template:/,
        qr/^MediaWiki:/,
        qr/^Portal:/,
        qr/^\d+月\d+日$/,
        qr/曖昧さ回避/, qr/^常用漢字$/) {
        if ($title =~ $re) {
            $skip_logger->("Skip due to title contains $re($title)");
            return [];
        }
    }

    # TODO: TITLE<<名古屋駅>> KANJI<<名古屋駅#名駅（めいえき）|名駅>> YOMI<<めいえき>> 4
    # TODO: TITLE<<日本酒>> KANJI<<&amp;#37211;>> YOMI<<もと>> 2
    # TODO: TITLE<<日本酒>> KANJI<<&amp;#37211;桶>> YOMI<<もとおけ>> 4
    # TODO: TITLE<<日本酒>> KANJI<<生&amp;#37211;系>> YOMI<<きもとけい>> 5
    # TODO: TITLE<<日本酒>> KANJI<<無ろ過|濾過酒>> YOMI<<むろかしゅ>> 5
    # TODO: TITLE<<武士>> KANJI<<武者(※本項へのリダイレクト暫定回避)|武者>> YOMI<<むしゃ>> 3
    # TODO: TITLE<<プロジェクト:日本の市町村>> KANJI<<○○市町村>> YOMI<<ふりがな>> 4
    # TODO: TITLE<<阪口大助>> KANJI<<「れべる☆じゃんぷ」>> YOMI<<ぽんちゃん>> 5
    # TODO: TITLE<<イタリアのユーロ硬貨>> KANJI<<&amp;#8364;2の縁>> YOMI<<へり>> 2
    # TODO: TITLE<<四字熟語>> KANJI<<#成語|成語>> YOMI<<せいご>> 3
    # TODO: TITLE<<擬態>> KANJI<<ヘンリー・ウォルター・ベイツ|ベイツ型擬態>> YOMI<<べいつがたぎたい>> 8
    # TODO: TITLE<<擬態>> KANJI<<フリッツ・ミューラー|ミューラー型擬態>> YOMI<<みゅーらーがたぎたい>> 10
    # TODO: TITLE<<儀鳳暦>> KANJI<<麟徳暦:zh:麟德曆|（中国語）>> YOMI<<りんとくれき>> 6
    # TODO: TITLE<<フィンランドのユーロ硬貨>> KANJI<<&amp;#8364;2の縁>> YOMI<<へり>> 2
    # TODO: TITLE<<フィンランドのユーロ硬貨>> KANJI<<&amp;#8364;2の縁>> YOMI<<へり>> 2
    # TODO: TITLE<<苦竹駅>> KANJI<<新田駅(宮城電気鉄道)|新田駅>> YOMI<<しんでんえき>> 6
    # TODO: TITLE<<江頭2:50>> KANJI<<江頭2&lt;nowiki&gt;:&lt;/nowiki&gt;50>> YOMI<<えがしらにじごじっぷん>> 11
    # TODO: TITLE<<ロンドンブーツ1号2号>> KANJI<<田村淳|田村淳>> YOMI<<たむらあつし>> 6
    # TODO: TITLE<<ロンドンブーツ1号2号>> KANJI<<田村亮(お笑い芸人)|田村亮>> YOMI<<たむらりょう>> 6
    # TODO: TITLE<<三重エフエム放送>> KANJI<<radio&lt;sup&gt;3&lt;/sup&gt;（レディオキューブFM三重）>> YOMI<<れでぃおきゅーぶえふえむみえ>> 14
    # TODO: TITLE<<瓢箪山駅 (大阪府)>> KANJI<<瓢{{lang|ja|簞}}山駅>> YOMI<<ひょうたんやまえき>> 9
    # TODO: TITLE<<東リ>> KANJI<<東リ株式会社>> YOMI<<とうり>> 3
    # TODO: TITLE<<東京っ子NIGHTお遊びジョーズ!!>> KANJI<<GAGROOM1134>> YOMI<<はがきねたのこーなー>> 10
    # TODO: TITLE<<カワサキ・GPZ400R>> KANJI<<カワサキ・GPZ400R>> YOMI<<じーぴーぜっとよんひゃくあーる>> 15
    # TODO: TITLE<<上市場駅>> KANJI<<三信上市場停留所|停留場>> YOMI<<さんしんかみいちばていりゅうじょう>> 17
    # TODO: TITLE<<狸御殿>> KANJI<<1.『狸御殿(1939年の映画)|狸御殿』>> YOMI<<たぬきごてん>> 6
    my @results;
    my $entries = W::parse_body($page);
    LOOP_ENTRY: for my $entry (@$entries) {
        my ($kanji, $yomi) = @$entry;

        for my $re (
            qr/^\p{Hiragana}+$/,
            qr/\[/,
            qr/^\d+(月|世紀|年代)$/,
            qr/^.$/, # 一文字の漢字は、SKK-JISYO.L に入ってるので除外。
            qr/^\d+月\d+日 (旧暦)$/,
            qr/^\d+$/, # TITLE<<Intel 4004>> KANJI<<4004>> YOMI<<よんまるまるよん>> 8
            qr/\{\{仮リンク/, # TITLE<<四川省>> KANJI<<{{仮リンク|巴蜀(歴史)|zh|巴蜀|label=巴蜀}}>> YOMI<<はしょく>> 4
            qr/^日本の企業一覧/, # TITLE<<日本の企業一覧 (その他製品)>> KANJI<<日本の企業一覧(その他製造)>> YOMI<<にほんのきぎょういちらんそのたせいぞう>> 19
            qr/の登場人物$/, # TITLE<<ときめきメモリアル2の登場人物>> KANJI<<ときめきメモリアル2の登場人物>> YOMI<<ときめきめもりあるつーのとうじょうじんぶつ>> 21
            qr{/}, # '''Keyboard / kAoru ikArAshi / 五十嵐 馨'''（いからし かおる）
        ) {
            if ($kanji =~ $re) {
                $skip_logger->("Skip due to kanji contains $re(kanji=$kanji, yomi=$yomi, title=$title)");
                next LOOP_ENTRY;
            }
        }

        for my $re (
            qr/^(本名|作画)：/,
            qr/・/,
            qr/、/,
            qr/^-/,
            qr/^または$/,
            qr/^.$/, # 一文字のよみは、ノイズの可能性が高い。
        ) {
            if ($yomi =~ $re) {
                $skip_logger->("Skip due to yomi contains $re(kanji=$kanji, yomi=$yomi, title=$title)");
                next LOOP_ENTRY;
            }
        }
        unless ($yomi =~ qr/^\p{Hiragana}+$/) {
            $skip_logger->("Skip due to yomi doesn't contain hiragana(yomi=$yomi, kanji=$kanji, title=$title)");
            next LOOP_ENTRY;
        }
        next if length($kanji) == 0;

        push @results, [$title, $kanji, $yomi];
    }
    return \@results;
}

1;

