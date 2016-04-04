from spack import *

class PyCython(Package):
    """The Cython compiler for writing C extensions for the Python language."""
    homepage = "https://pypi.python.org/pypi/cython"
    url      = "https://pypi.python.org/packages/source/C/Cython/Cython-0.22.tar.gz"

    version('0.23.5', '66b62989a67c55af016c916da36e7514')
    version('0.23.4', '157df1f69bcec6b56fd97e0f2e057f6e')

    # These versions contain illegal Python3 code...
    version('0.22', '1ae25add4ef7b63ee9b4af697300d6b6')
    version('0.21.2', 'd21adb870c75680dc857cd05d41046a4')

    extends('python')
    depends_on('binutils')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
