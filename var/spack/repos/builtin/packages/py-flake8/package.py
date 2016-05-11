from spack import *


class PyFlake8(Package):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""
    homepage = "http://flake8.readthedocs.io/en/latest/"
    url      = "https://pypi.python.org/packages/source/f/flake8/flake8-2.5.4.tar.gz"

    version('2.5.4', 'a4585b3569b95c3f66acb8294a7f06ef')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
