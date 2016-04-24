from spack import *

class PyDbf(Package):
    """
    Pure python package for reading/writing dBase, FoxPro, and Visual FoxPro
    .dbf files (including memos).
    """

    homepage = 'https://pypi.python.org/pypi/dbf'
    url      = "https://pypi.python.org/packages/source/d/dbf/dbf-0.96.005.tar.gz"

    version('0.96.005', 'bce1a1ed8b454a30606e7e18dd2f8277')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
