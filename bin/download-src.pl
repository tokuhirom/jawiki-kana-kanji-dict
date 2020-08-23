use strict;
use warnings;
use utf8;
use LWP::UserAgent;
use File::Path qw(make_path remove_tree);

make_path('src');

my $srcurl = 'https://dumps.wikimedia.org/jawiki/latest/';
my $ua = LWP::UserAgent->new();
my $res = $ua->get($srcurl);
$res->is_success or die $res->status_line;
my $content = $res->content;
my %seen;
while ($content =~ s{(jawiki-latest-pages-articles\d+.xml.+?.bz2)}{}) {
    my $fname = $1;
    next if $seen{$fname}++;

    print "Downloading $fname\n";
    $ua->show_progress(1);
    my $res = $ua->mirror("$srcurl/$fname", "src/$fname");
    print "Downloaded $fname: @{[ $res->status_line ]}\n";
}

