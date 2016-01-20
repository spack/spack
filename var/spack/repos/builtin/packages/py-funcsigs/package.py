from spack import *
import os

class PyFuncsigs(Package):
    """Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2."""
    homepage = "https://pypi.python.org/pypi/funcsigs"
    url      = "https://pypi.python.org/packages/source/f/funcsigs/funcsigs-0.4.tar.gz"

    version('0.4', 'fb1d031f284233e09701f6db1281c2a5')

    extends('python')

    depends_on('py-setuptools')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)



