# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SOURCEDIR     = docs/source
BUILDDIR      = docs
MODULEDIR     = st3

.PHONY: source clean

source:
	SPHINX_APIDOC_OPTIONS=members,no-special-members sphinx-apidoc --separate --force --no-toc -o "$(SOURCEDIR)/modules" "$(MODULEDIR)"

html:
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf docs/source/modules docs/doctrees docs/html
