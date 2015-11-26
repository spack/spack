from spack import *

class PyMock(Package):
    """mock is a library for testing in Python. It allows you to replace parts
    of your system under test with mock objects and make assertions about how
    they have been used."""

    homepage = "https://github.com/testing-cabal/mock"
    url      = "https://pypi.python.org/packages/source/m/mock/mock-1.3.0.tar.gz"

    version('1.3.0', '73ee8a4afb3ff4da1b4afa287f39fdeb')

    extends('python')
    depends_on('py-setuptools@17.1:')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
