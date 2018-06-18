# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = sublime_lib
SOURCEDIR     = docs/source
BUILDDIR      = docs
MODULEDIR     = st3

.PHONY: Makefile source clean

source:
	SPHINX_APIDOC_OPTIONS=members,no-special-members sphinx-apidoc --separate --force --no-toc -o "$(SOURCEDIR)/modules" "$(MODULEDIR)"

html:
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf docs/source/modules docs/doctrees docs/html
