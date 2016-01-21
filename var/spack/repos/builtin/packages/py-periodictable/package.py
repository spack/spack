from spack import *

class PyPeriodictable(Package):
    """nose extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/periodictable"
    url      = "https://pypi.python.org/packages/source/p/periodictable/periodictable-1.4.1.tar.gz"

    version('1.4.1', '7246b63cc0b6b1be6e86b6616f9e866e')

    depends_on('py-numpy')
    depends_on('py-pyparsing')
    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
