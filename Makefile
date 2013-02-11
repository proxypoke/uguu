.PHONY: all
all:
	@make man

.PHONY: html
doc:
	a2x --doctype xhtml --format manpage README.asciidoc

.PHONY: man
man:
	a2x --doctype manpage --format manpage README.asciidoc -D man
	gzip -f man/*

.PHONY: clean
clean:
	rm -f *.pyc
	rm -f *.pyo
	rm -f *.log
	rm -rf __pycache__

.PHONY: mrproper
mrproper:
	rm -f man/* --interactive=never
	rm -f *.sqlite
	make clean
	rm -rf dist
	python setup.py clean
