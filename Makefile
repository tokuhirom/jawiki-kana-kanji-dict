all: jawiki-latest-pages-articles.xml.bz2

jawiki-latest-pages-articles.xml.bz2:
	wget -nc https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

.PHONY: all
