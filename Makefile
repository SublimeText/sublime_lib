# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SOURCEDIR     = docs/source
BUILDDIR      = docs

.PHONY: clean

html:
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf doctrees html
