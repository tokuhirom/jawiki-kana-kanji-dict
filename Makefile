all: SKK-JISYO.jawiki

clean:
	rm -f dat/*.tsv

check: SKK-JISYO.jawiki
	pytest check.py

test:
	pytest
	pyflakes *.py */*.py
	autopep8 --max-line-length 180 -i *.py */*.py
	flake8 . --count --exit-zero --max-complexity=30 --max-line-length=1200 --statistics

dat/jawiki-latest-pages-articles.xml.bz2:
	wget --no-verbose --no-clobber -O dat/jawiki-latest-pages-articles.xml.bz2 https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

dat/jawiki-latest-pages-articles.xml: dat/jawiki-latest-pages-articles.xml.bz2
	bunzip2 --keep dat/jawiki-latest-pages-articles.xml.bz2

dat/grepped.txt: dat/jawiki-latest-pages-articles.xml
	grep -E "<title>.*</title>|'''[』|（(]" dat/jawiki-latest-pages-articles.xml > dat/grepped.txt

dat/scanned.tsv: dat/grepped.txt scanner.py jawiki/scanner.py
	python scanner.py

dat/pre_validated.tsv: dat/scanned.tsv pre_validator.py jawiki/pre_validate.py
	python pre_validator.py

dat/converted.tsv: dat/pre_validated.tsv converter.py jawiki/converter.py jawiki/hojin.py jawiki/jachars.py
	python converter.py

dat/post_validated.tsv: dat/converted.tsv post_validator.py jawiki/post_validate.py user_simpledic.csv
	python post_validator.py

SKK-JISYO.jawiki: dat/post_validated.tsv makedict.py
	python makedict.py /usr/share/skk/SKK-JISYO.L /usr/share/skk/SKK-JISYO.jinmei /usr/share/skk/SKK-JISYO.geo

.PHONY: all test check

