from spack import *
import re

class PyNumexpr(Package):
    """Fast numerical expression evaluator for NumPy"""
    homepage = "https://pypi.python.org/pypi/numexpr"
    url      = "https://pypi.python.org/packages/source/n/numexpr/numexpr-2.4.6.tar.gz"

    version('2.4.6', '17ac6fafc9ea1ce3eb970b9abccb4fbd')
    version('2.5', '84f66cced45ba3e30dcf77a937763aaa')

    extends('python', ignore=r'bin/f2py$')
    depends_on('py-numpy')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
