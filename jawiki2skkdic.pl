#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

use lib 'lib';
use W;

use Encode;
use Pod::Usage;
use Term::ANSIColor;

use IO::Uncompress::Bunzip2 qw/$Bunzip2Error/;

binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

my $srcfile = shift @ARGV or pod2usage;

my $z = IO::Uncompress::Bunzip2->new($srcfile)
        or die "bunzip2 failed: $Bunzip2Error\n";

my $DEBUG = 0;

&main; exit;

sub main {
    my $buffer;
    my $readcnt;
    LOOP: while (1) {
        my $buf;
        my $status = $z->read($buf, 10*1024*1024);
        $buffer .= $buf;
        print "    [DEBUG] READ $readcnt @{[ length($buffer) ]}\n" if $readcnt++;

        my $decoded = eval { Encode::decode('utf-8', $buffer, Encode::FB_CROAK) };
        next if $@;
        warn "    [DEBUG] Decoded @{[ length($decoded) // '-' ]} @{[ $@ // 'NO_ERROR' ]}\n";

        LOOP_PAGE: while ($decoded =~ s!<page>(.+?)</page>!!s) {
            my $page = $1;
            my $title = W::parse_title($page);
            for my $re (
                qr/一覧$/, # '国の一覧' or 'ゲーム会社一覧'
                qr/^Wikipedia:/,
                qr/^\d+月\d+日$/, qr/曖昧さ回避/, qr/^常用漢字$/) {
                if ($title =~ $re) {
                    print colored(['yellow'], "   [DEBUG] Skip due to title contains $re($title)\n");
                    next LOOP_PAGE;
                }
            }

            my @results = W::parse_body($page);
            LOOP_ENTRY: for my $result (@results) {
                my ($kanji, $yomi) = @$result;

                for my $re (
                    qr/^\p{Hiragana}+$/,
                    qr/\[/,
                    qr/^\d+(月|世紀|年代)$/,
                    qr/^.$/,
                ) {
                    if ($kanji =~ $re) {
                        print colored(['yellow'], "   [DEBUG] Skip due to kanji contains $re(kanji=$kanji, yomi=$yomi)\n");
                        next LOOP_ENTRY;
                    }
                }

                for my $re (
                    qr/^(本名|作画)：/,
                    qr/・/,
                    qr/^-/,
                    qr/^または$/,
                ) {
                    if ($yomi =~ $re) {
                        print colored(['yellow'], "   [DEBUG] Skip due to yomi contains $re(kanji=$kanji, yomi=$yomi)\n");
                        next LOOP_ENTRY;
                    }
                }
                unless ($yomi =~ qr/^\p{Hiragana}+$/) {
                    print colored(['yellow'], "   [DEBUG] Skip due to yomi contains is not hiragana(yomi=$yomi, kanji=$kanji, title=$title)\n");
                    next LOOP_ENTRY;
                }

                print("TITLE<<@{[ $title ]}>> KANJI<<$kanji>> YOMI<<$yomi>> @{[ length($yomi) ]}\n");
            }
        }
    }
}


__END__

=head1 SYNOPSIS

    $ perl jawiki.skkdic.pl jawiki-latest-pages-articles.xml.bz2


