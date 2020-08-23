#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use YAML;
use List::Util qw/uniq/;
use Pod::Usage;

use lib 'lib';
use autodie;

binmode( STDOUT, ":utf8" );
binmode( STDERR, ":utf8" );

&main;exit;

sub main {
    my $skkdictpath = shift @ARGV or pod2usage();

    my %dict;
    for my $src (<extracted/*.dict>) {
        open my $fh, '<:utf8', $src;
        while (<$fh>) {
            if (m{KANJI:<<<(.+)>>>\s+YOMI:<<<(.+)>>>\s+TITLE:<<<(.+)>>>}) {
                my ($kanji, $yomi) = ($1, $2);
                push @{$dict{$yomi}}, $kanji;
            }
        }
    }

    open my $ofh, '>:utf8', 'SKK-JISYO.jawiki';

    my $skkdict = parse_skkdic($skkdictpath);

    # exclude some special entries
    # あふがにすたんふんそう /アフガニスタン紛争（2001年-現在）/1979年-1989年のアフガニスタン紛争/アフガニスタン紛争/
    delete $dict{qw/あふがにすたんふんそう/};
    # '''伊東彦兵衛尉藤原祐信（すけのぶ）伊東 祐信'''（いとう すけのぶ）は、[[室町時代]]の武士。
    delete $dict{qw/いとうすけのぶ/};
    # '''[[鹿野町 (山口県)]]'''（かの）
    delete $dict{qw/かの/};

    for my $yomi (sort keys %dict) {
        # 特殊記号始まりの読みになっているものを除外する
        next if $yomi =~ /^[〜『「〈《]/;

        my @kanji = grep { ! $skkdict->{$yomi}{$_} } uniq @{$dict{$yomi}};
        next unless @kanji;
        printf {$ofh} "%s /%s/\n", $yomi, join('/', @kanji);
    }
    close $ofh;
}

sub parse_skkdic {
    my $dictpath = shift;

    open my $dictfh, '<:encoding(euc-jp)', $dictpath;
    my %matched;
    while (<$dictfh>) {
        chomp;
        next if /^;;/;

        my ($yomi, $kanji) = split / /, $_, 2;
        unless (defined $kanji) {
            warn "++ $_ ++";
        }
        $kanji =~ s!^/!!;
        $kanji =~ s!/$!!;
        my @kanji = map {
            my $x = $_;
            $x =~ s/;.*//;
            $x;
        } split m{/}, $kanji;
        for my $kanji (@kanji) {
            $matched{$yomi}{$kanji}++;
        }
    }
    return \%matched;
}

__END__

=head1 SYNOPSIS

    $ perl bin/extracted2skkdic.pl

