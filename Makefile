all: SKK-JISYO.jawiki

clean:
	rm -f jawiki-latest-pages-articles.xml.bz2 jawiki-latest-pages-articles.xml scanned.tsv filtered.tsv SKK-JISYO.jawiki skipped.tsv

test:
	python -m unittest tests/test_filter.py
	pytest tests/pytest_filter.py

jawiki-latest-pages-articles.xml.bz2:
	wget -nc https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

jawiki-latest-pages-articles.xml: jawiki-latest-pages-articles.xml.bz2
	bunzip2 --keep jawiki-latest-pages-articles.xml.bz2

scanned.tsv: jawiki-latest-pages-articles.xml scanner.py
	python scanner.py jawiki-latest-pages-articles.xml

filtered.tsv: scanned.tsv filter.py jawiki/filter.py
	python filter.py scanned.tsv

SKK-JISYO.jawiki: filtered.tsv makedict.py /usr/share/skk/SKK-JISYO.L
	python makedict.py /usr/share/skk/SKK-JISYO.L

.PHONY: all test

