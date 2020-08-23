#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use YAML;
use List::Util qw/uniq/;

use lib 'lib';
use autodie;

binmode( STDOUT, ":utf8" );
binmode( STDERR, ":utf8" );

&main;exit;

sub main {
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

    # TODO: load SKK-JISYO.L

    # exclude some special entries
    # あふがにすたんふんそう /アフガニスタン紛争（2001年-現在）/1979年-1989年のアフガニスタン紛争/アフガニスタン紛争/
    delete $dict{qw/あふがにすたんふんそう/};

    for my $yomi (sort keys %dict) {
        # 特殊記号始まりの読みになっているものを除外する
        next if $yomi =~ /^[〜『「]/;

        printf {$ofh} "%s /%s/\n", $yomi, join('/', uniq @{$dict{$yomi}});
    }
    close $ofh;
}

