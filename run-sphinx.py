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
import sys


####################################################################################################
#
# Sanity checks


script_dir = os.path.dirname(os.path.realpath(__file__))

if os.getcwd() != script_dir:
    print >>sys.stderr, "run-sphinx.py: to avoid confusion, the current working directory must be the same as the directory containing the script"
    print >>sys.stderr, "    (cwd='%s', script_dir='%s')" % (os.getcwd(), script_dir)
    sys.exit(1)

#for f in [ "sphinx/index.rst", "docs/index.html" ]:
#    if not os.path.exists(f):
#        print >>sys.stderr, "run-sphinx.py: file '%s' does not exist ?!" % f
#        sys.exit(1)


####################################################################################################


def xsystem(cmd, show=True):
    if show:
        print '+', cmd

    if os.system(cmd):
        print >>sys.stderr, "Shell command failed:", cmd
        sys.exit(1)


# The -E flag forces 'sphinx-build' to reread all its input files, even if nothing
# appears to have changed.  This is necessary because 'sphinx-build' has no way of
# knowing if docstrings have been changed since last time.

xsystem("sphinx-build -E -b html sphinx docs")


# The only thing I don't like about the RTD Sphinx theme is that it doesn't put any
# spacing between bullet points in unordered lists.  I got carried away and wrote
# this code to hack the Sphinx-generated CSS!

with open('docs/_static/css/theme.css', 'a') as f:
    maxdepth = 9
    print >>f, "ul li { margin: 10px 0; }"
    for d in xrange(1, maxdepth+1):
        print >>f, "li.toctree-l%d { margin: 0 0; }" % d


print
print 'A local copy of the documentation has been built successfully!'
print 'To view it, point your web browser here:'
print
print '    file://%s' % os.path.join(os.getcwd(), 'docs/index.html')

# Traverse 'docs' directory looking for missing .nojekyll files.
# My understanding is that every directory which contains subdirectories must contain .nojekyll.

dirs_already_checked = set([''])

def check_nojekyll(opaque_arg, dirname, fnames):
    if dirname.startswith('docs/.doctrees') or dirname.startswith('docs/.buildinfo'):
        return
    parent = os.path.dirname(dirname)
    if parent not in dirs_already_checked:
        if not os.path.exists(os.path.join(parent, '.nojekyll')):
            print "*** WARNING: directory '%s' does not contain the .nojekyll file (required by Github Pages)" % parent
        dirs_already_checked.add(parent)

os.path.walk('docs', check_nojekyll, None)
