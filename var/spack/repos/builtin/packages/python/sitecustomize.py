"""
Hack a bunch of directories onto the front of sys.path
"""

import os
import site

## Need to find the `.python-sitedirs` file.
## But, sys.argv hasn't been set up yet.
# Here's one way, from :
# https://bugs.python.org/issue2972
# WTD on things w/out `/proc/self/cmdline` (e.g. OS X)?
cmdline = open("/proc/self/cmdline").read()
cmd = cmdline.split('\x00')[1]

## # Here's an alternative
## # from here: https://stackoverflow.com/questions/6485678/how-can-i-get-the-name-file-of-the-script-from-sitecustomize-py
## # Create a little class with a destructor, assign it to sys.argv
## # and the destructor will be called when sys.argv gets its real value
## # (SHUDDER...)
## class Yikes(object):
##     def __del__(self):
##         # e.g.
##         # commandline = " ".join(sys.argv)
##         # grab the script name from the newly populated sys.argv
##         # find the .python-sitedirs file and add its contents to sys.path
##         # with site.addsitedir(...).
## sys.argv = Yikes()

try:
    sd_file = os.path.join(os.path.dirname(cmd), ".python-sitedirs")
    sitedirs = open(sd_file).read()

    for d in sitedirs.split():
        site.addsitedir(os.path.join(d, 'lib', 'python2.7', 'site-packages'))
except:
    # no IO available, there's nothing to be done
    pass
