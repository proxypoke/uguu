.PHONY: all
all:
	@make man

.PHONY: html
doc:
	a2x --doctype xhtml --format manpage README.asciidoc

.PHONY: man
man:
	a2x --doctype manpage --format manpage README.asciidoc

.PHONY: clean
clean:
	rm -f *.1
	rm -f *.pyc
	rm -f *.pyo
	rm -f *.log

.PHONY: mrproper
mrproper:
	rm -f *.sqlite
	make clean
