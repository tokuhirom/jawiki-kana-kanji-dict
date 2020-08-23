use strict;
use warnings;
use utf8;
use autodie;
use LWP::UserAgent;
use File::Path qw(make_path remove_tree);
use File::Basename qw/basename/;
use Time::Piece;

&main; exit;

sub main {
    make_path('src');
    get_file_list();
}

sub get_file_list {
    unlink 'src/_SUCCESS' if -e 'src/_SUCCESS';

    my $srcurl = 'https://dumps.wikimedia.org/jawiki/latest/';
    my $ua = LWP::UserAgent->new();
    my $res = $ua->get($srcurl);
    $res->is_success or die $res->status_line;
    my $content = $res->content;
    my %filenames;
    while ($content =~ s{(jawiki-latest-pages-articles\d+.xml.+?.bz2)}{}) {
        my $fname = $1;
        next if $filenames{$fname}++;
    }

    # cleanup files not in the index.
    {
        my @files = map { basename($_) } <src/*.bz2>;
        for my $file (@files) {
            unless ($filenames{$file}) {
                print "Unlink src/$file\n";
                unlink "src/$file";
            }
        }
    }

    # enable progress bar
    $ua->show_progress(1);

    for my $fname (keys %filenames) {
        print "Downloading $fname\n";
        my $res = $ua->mirror("$srcurl/$fname", "src/$fname");
        print "Downloaded $fname: @{[ $res->status_line ]}\n";
    }

    # bunzip2
    system('/bin/ls src/*.bz2 | xargs bunzip2 --verbose --keep')
        == 0 or die "Cannot extract bzip2";

    open my $fh, '>', 'src/_SUCCESS'
        or die "Cannot open src/_SUCCESS file";
    for my $fname (keys %filenames) {
        my $f = $fname;
        $f =~ s/\.bz2$//;
        print {$fh} "src/$f\n";
    }
    close $fh;
}

