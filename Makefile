all: SKK-JISYO.jawiki

clean:
	rm -f jawiki-latest-pages-articles.xml.bz2 jawiki-latest-pages-articles.xml grepped.txt scanned.tsv filtered.tsv SKK-JISYO.jawiki skipped.tsv pre_validated.tsv

check: SKK-JISYO.jawiki
	pytest check.py

test:
	pytest
	pyflakes *.py */*.py
	autopep8 --max-line-length 180 -i *.py */*.py
	flake8 . --count --exit-zero --max-complexity=30 --max-line-length=1200 --statistics

jawiki-latest-pages-articles.xml.bz2:
	wget --no-verbose --no-clobber https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

jawiki-latest-pages-articles.xml: jawiki-latest-pages-articles.xml.bz2
	bunzip2 --keep jawiki-latest-pages-articles.xml.bz2

grepped.txt: jawiki-latest-pages-articles.xml
	grep -E "<title>.*</title>|'''[』|（(]" jawiki-latest-pages-articles.xml > grepped.txt

scanned.tsv: grepped.txt scanner.py jawiki/scanner.py
	python scanner.py grepped.txt

pre_validated.tsv: scanned.tsv pre_validator.py jawiki/pre_validate.py
	python pre_validator.py

filtered.tsv: pre_validated.tsv filter.py jawiki/filter.py jawiki/hojin.py jawiki/jachars.py
	python filter.py pre_validated.tsv

SKK-JISYO.jawiki: filtered.tsv makedict.py /usr/share/skk/SKK-JISYO.L
	python makedict.py /usr/share/skk/SKK-JISYO.L /usr/share/skk/SKK-JISYO.jinmei /usr/share/skk/SKK-JISYO.geo

.PHONY: all test check

