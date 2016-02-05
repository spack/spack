from spack import *

class PyWheel(Package):
    """A built-package format for Python."""

    homepage = "https://pypi.python.org/pypi/wheel"
    url      = "https://pypi.python.org/packages/source/w/wheel/wheel-0.26.0.tar.gz"

    version('0.26.0', '4cfc6e7e3dc7377d0164914623922a10')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
