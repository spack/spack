from spack import *

class PyPmw(Package):
    """Pmw is a toolkit for building high-level compound widgets, or megawidgets, constructed using other widgets as component parts."""
    homepage = "https://pypi.python.org/pypi/Pmw"
    url      = "https://pypi.python.org/packages/source/P/Pmw/Pmw-2.0.0.tar.gz"

    version('2.0.0', 'c7c3f26c4f5abaa99807edefee578fc0')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
