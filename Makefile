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

dat/jawiki-latest-pages-articles.xml:
	curl -s https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 | bunzip2 > dat/jawiki-latest-pages-articles.xml

dat/grepped.txt: dat/jawiki-latest-pages-articles.xml
	grep -E "<title>.*</title>|'''[』|（(]" dat/jawiki-latest-pages-articles.xml > dat/grepped.txt

dat/scanned.tsv: dat/grepped.txt bin/scanner.py jawiki/scanner.py
	python bin/scanner.py

dat/pre_validated.tsv: dat/scanned.tsv bin/pre_validator.py jawiki/pre_validate.py
	python bin/pre_validator.py

dat/converted.tsv: dat/pre_validated.tsv bin/converter.py jawiki/converter.py jawiki/hojin.py jawiki/jachars.py
	python bin/converter.py

dat/post_validated.tsv: dat/converted.tsv bin/post_validator.py jawiki/post_validate.py user_simpledic.csv
	python bin/post_validator.py

SKK-JISYO.jawiki: dat/post_validated.tsv bin/makedict.py jawiki/skkdict.py
	python bin/makedict.py /usr/share/skk/SKK-JISYO.L /usr/share/skk/SKK-JISYO.jinmei /usr/share/skk/SKK-JISYO.geo

.PHONY: all test check

