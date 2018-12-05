#!/usr/bin/env python
#
# This script will run 'sphinx-build' to generate static web pages in docs/
# from the .rst and image files in sphinx/.
#
#   - After the script has run, you can browse a local copy of the documentation
#     by pointing your browser to docs/index.html.
#
#   - To publish your local copy to the web (https://kmsmith137.github.io/ch_frb_l1_docs/), 
#     just do git add/commit/push as usual.  I try not to do this too frequently, to avoid 
#     bloating the docs repo.  (For example, 'docs/search.js' basically gets rewritten 
#     every time the docs get updated.)


import os
import sphinx_helpers

toplevel_dir = os.path.dirname(os.path.realpath(__file__))
print 'Running sphinx in directory', toplevel_dir

sphinx_helpers.run_sphinx(toplevel_dir)
