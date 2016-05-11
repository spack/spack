from spack import *


class PyPathspec(Package):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/pathspec"

    version('0.3.4', '2a4af9bf2dee98845d583ec61a00d05d',
        url='https://pypi.python.org/packages/14/9d/c9d790d373d6f6938d793e9c549b87ad8670b6fa7fc6176485e6ef11c1a4/pathspec-0.3.4.tar.gz')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
