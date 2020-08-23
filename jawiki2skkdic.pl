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
        my $status = $z->read($buf, 100*1024*1024);
        $buffer .= $buf;
        print STDERR "#   [DEBUG] READ $readcnt @{[ length($buffer) ]}\n" if $readcnt++;

        my $decoded = eval { Encode::decode('utf-8', $buffer, Encode::FB_CROAK) };
        next if $@;
        warn "#   [DEBUG] Decoded @{[ length($decoded) // '-' ]} @{[ $@ // 'NO_ERROR' ]}\n";

        LOOP_PAGE: while ($decoded =~ s!<page>(.+?)</page>!!s) {
            my $results = W::parse_page($1);
            for my $result (@$results) {
                my ($title, $kanji, $yomi) = @$result;
                printf "%-30s %-30s %-30s\n",
                    "KANJI:<<<$kanji>>>", "YOMI:<<<$yomi>>>", "TITLE:<<<$title>>>";
            }
        }
    }
}


__END__

=head1 SYNOPSIS

    $ perl jawiki.skkdic.pl jawiki-latest-pages-articles.xml.bz2


