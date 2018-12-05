### sphinx_helpers

A small python module of helper functions for maintaining Sphnix documentation, which
I include in larger doc repositories as a git subtree.  Assumes my pet directory layout
(toplevel sphinx files are sphinx/conf.py and sphinx/index.rst, toplevel HTML file is
docs/index.html).

```
cd PROJNAME_DOCS
git subtree add --squash --prefix=sphinx_helpers github:kmsmith137/sphinx_helpers master

mkdir sphinx   # sphinx input directory, containing .rst files
mkdir docs     # sphinx output directory, containing .html files

# Generate sphinx/conf.py.
# Here, IMPORT_DIRS is one or more directories to be added to python sys.path.
# I often use IMPORT_DIRS=../PROJNAME (assuming parallel directories PROJNAME and PROJNAME_DOCS)
sphinx_helpers/make_sphinx_conf.py PROJNAME [IMPORT_DIRS] > sphinx/conf.py

# Edit appropriately
emacs sphinx/index.rst

# Edit appropriately (for a template, copy from e.g. simpulse_docs/run-sphinx.py)
emacs run-sphinx.py
```
