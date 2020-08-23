all: SKK-JISYO.jawiki

clean:
	rm -f src/_SUCCESS extracted/_SUCCESS SKK-JISYO.jawiki

test:
	prove -lr t/

distclean:
	rm -rf src/ extracted/

src/_SUCCESS:
	perl bin/download-src.pl

extracted/_SUCCESS: src/_SUCCESS
	perl bin/extract.pl

SKK-JISYO.jawiki: extracted/_SUCCESS
	perl bin/extracted2skkdic.pl

.PHONY: all distclean test

