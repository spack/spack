from spack import *

class PyCython(Package):
    """The Cython compiler for writing C extensions for the Python language."""
    homepage = "https://pypi.python.org/pypi/cython"
    url      = "https://pypi.python.org/packages/source/C/Cython/cython-0.22.tar.gz"

    version('0.21.2', 'd21adb870c75680dc857cd05d41046a4')
    version('0.22', '1ae25add4ef7b63ee9b4af697300d6b6')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
