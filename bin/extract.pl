#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

use lib 'lib';
use W;
use autodie;

use Encode;
use Pod::Usage;
use Term::ANSIColor;
use Parallel::ForkManager;
use File::Basename qw/basename/;
use File::Path qw(make_path remove_tree);
use IO::Handle;
use Time::HiRes qw/gettimeofday tv_interval/;
use Log::Minimal;

use IO::Uncompress::Bunzip2 qw/$Bunzip2Error/;

binmode( STDOUT, ":utf8" );
binmode( STDERR, ":utf8" );

my $DEBUG = 0;

&main;
exit;

sub main {
    make_path('extracted');
    make_path('log');

    my @filenames = load_src_list();
    run_processes(@filenames);
}

sub load_src_list {
    open my $fh, '<', 'src/_SUCCESS';
    my $src = do { local $/; <$fh> };
    return grep /\S/, split /\n/, $src;
}

sub run_processes {
    my @filenames = @_;

    my $pm = Parallel::ForkManager->new(8);

    my $skiplogfile = "log/skip.log";
    open my $skipfh, '>:encoding(utf-8)', $skiplogfile
      or die "Cannot open $skiplogfile: $!";
    $skipfh->autoflush(1);

    my $skip_logger = sub {
        my $msg = join(" ", @_);
        print {$skipfh} "[$$] $msg\n";
    };

  DATA_LOOP:
    foreach my $srcfile (@filenames) {
        my $pid = $pm->start and next DATA_LOOP;

        $0 = "jawiki2skkdic.pl [$srcfile]";

        my $t0 = [gettimeofday];

        my $dstfile = get_dst_file($srcfile);
        run( $skip_logger, $srcfile, $dstfile );

        print STDERR "[$$] Finished processing $srcfile in @{[ tv_interval($t0) ]}\n";

        $pm->finish;    # Terminates the child process
    }
    $pm->wait_all_children;

    open my $successfh, '>', 'extracted/_SUCCESS';
    print {$successfh} "OK";
    close $successfh;
}

sub get_dst_file {
    my $srcfile = shift;

    my $base = basename($srcfile);
    return "extracted/$base.dict";
}

sub commify {
    my $text = reverse $_[0];
    $text =~ s/(\d\d\d)(?=\d)(?!\d*\.)/$1,/g;
    return scalar reverse $text;
}

sub run {
    my ( $skip_logger, $srcfile, $dstfile ) = @_;

    open my $srcfh, '<:encoding(utf-8)', $srcfile;
    open my $fh, '>:encoding(utf-8)', $dstfile;

    my $t0 = [gettimeofday];

    my $buffer = '';
    my $total_size = -s $srcfile;
    my $read_size = 0;
    my $loopcnt;
  LOOP: while (!eof($srcfh)) {
        my $status = $srcfh->read( $buffer, 10 * 1024 * 1024, length($buffer) );
        if ($status == 0) {
            warn "#   [$$] [DEBUG] file handle reached EOF\n";
            last LOOP;
        }
        if (not defined $status) {
            die "#   [$$] [DEBUG] file handle throw an error: $!\n";
        }
        $read_size += $status;

        printf STDERR "#   [$$] %d [%-60s] READ %s/%s=%.2f%% remaining=%.2f sec\n",
            ++$loopcnt, $srcfile, commify($read_size), commify($total_size), 100.0*$read_size/$total_size,
            (tv_interval($t0) * ($total_size/$read_size)) - tv_interval($t0);

        my $n = 0;
      LOOP_PAGE: while ( $buffer =~ s!(.+?)</page>!!s ) {
            my $results = W::parse_page($1, $skip_logger);
            for my $result (@$results) {
                my ( $title, $kanji, $yomi ) = @$result;
                printf {$fh} "%-30s %-30s %-30s\n",
                  "KANJI:<<<$kanji>>>", "YOMI:<<<$yomi>>>",
                  "TITLE:<<<$title>>>";
            }
        }
    }
    printf {$fh} "---- FINISHED ----\n";
}

__END__

=head1 SYNOPSIS

    $ perl jawiki.skkdic.pl jawiki-latest-pages-articles.xml.bz2


