#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print >>sys.stderr, 'usage: make-sphinx-conf.py <project_name> [sys_path_entry1] [sys_path_entry2] ...'
    sys.exit(2)

projname = sys.argv[1]
sys_path_entries = sys.argv[2:]

print '# Autogenerated by make-sphinx-conf.py -- do not edit!'
print '# Command line:', (' '.join(sys.argv))
print 
print 'import os'
print 'import sys'
print 
print "# From command line"
print "project = u'%s'" % projname

for p in list(reversed(sys_path_entries)):
    print "sys.path.insert(0, os.path.abspath('%s'))" % p

print 
print "# Added by KMS"
print "autoclass_content = 'both'"
print "autodoc_default_flags = [ 'inherited-members' ]"
print "html_show_copyright = False"
print "html_show_sphinx = False"
print "html_show_sourcelink = False"
print 
print "# From sphinx-quickstart"
print "extensions = [ 'sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.autosectionlabel' ]"
print "source_suffix = '.rst'"
print "master_doc = 'index'"
print "html_theme = 'sphinx_rtd_theme'"
