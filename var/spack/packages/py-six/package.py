from spack import *

class PySix(Package):
    """Python 2 and 3 compatibility utilities."""
    homepage = "https://pypi.python.org/pypi/six"
    url      = "https://pypi.python.org/packages/source/s/six/six-1.9.0.tar.gz"

    version('1.9.0', '476881ef4012262dfc8adc645ee786c4')

    extends('python')
    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
