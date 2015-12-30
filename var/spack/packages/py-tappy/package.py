from spack import *

class PyTappy(Package):
    """Python TAP interface module for unit tests"""
    homepage = "https://github.com/mblayman/tappy"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://pypi.python.org/packages/source/t/tap.py/tap.py-1.6.tar.gz"

    version('1.6', 'c8bdb93ad66e05f939905172a301bedf')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
