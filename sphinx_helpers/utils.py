import os
import sys

def system(cmd, show=True):
    if show:
        print '+', cmd

    if os.system(cmd):
        print >>sys.stderr, "Shell command failed:", cmd
        sys.exit(1)
