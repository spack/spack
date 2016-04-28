from spack import *

class PySympy(Package):
    """SymPy is a Python library for symbolic mathematics."""
    homepage = "https://pypi.python.org/pypi/sympy"
    url      = "https://pypi.python.org/packages/source/s/sympy/sympy-0.7.6.tar.gz"

    version('0.7.6', '3d04753974306d8a13830008e17babca')
    version('1.0', '43e797de799f00f9e8fd2307dba9fab1')

    extends('python')
    depends_on('py-mpmath', when='@1.0:')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
