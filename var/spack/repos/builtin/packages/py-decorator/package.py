from spack import *

class PyDecorator(Package):
    """The aim of the decorator module it to simplify the usage of decorators for the average programmer, and to popularize decorators by showing various non-trivial examples."""
    homepage = "https://github.com/micheles/decorator"
    url      = "https://pypi.python.org/packages/source/d/decorator/decorator-4.0.9.tar.gz"

    version('4.0.9', 'f12c5651ccd707e12a0abaa4f76cd69a')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
