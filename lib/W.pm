package W;
use strict;
use warnings;
use utf8;
use 5.010_001;

use Lingua::JA::Regular::Unicode qw/katakana2hiragana/;
;

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

    my @results;

    while ($page =~ s/'''(.+?)'''（(.+?)）//) {
        my $kanji = $1;
        my $yomi  = $2;

        $yomi =~ s/\{\{lang-en-short\|.+?\}\}//g;
        $yomi =~ s/\{\{lang-en\|.+?\}\}//g;
        $yomi =~ s!&lt;ref&gt;.*!!g; # <ref>.*</ref>
        $yomi =~ s/&lt;!--.*--&gt;//g;
        $kanji =~ s/\{\{JIS2004フォント\|(.+)\}\}/$1/g; # '''司馬 {{JIS2004フォント|遼󠄁}}太郎'''

        # '''[[葉状体]]'''（ようじょうたい）
        # '''[[瘀血]]証'''（おけつしょう）
        $kanji =~ s!\[\[(.*)\]\]!$1!;

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

        # 、 以後は除去
        $yomi =~ s/、.*//;

        # 空白除去
        $kanji =~ s/ //g;
        $yomi =~ s/ //g;

        if ($kanji =~ /'''/) {
            debug("Skip: contains q/'''/");
            next;
        }

        debug("    CODE<<$kanji>> YOMI<<$yomi>> @{[ length($yomi) ]}\n");
        push @results, [$kanji, katakana2hiragana($yomi)];
    }
    return @results;
}

1;

