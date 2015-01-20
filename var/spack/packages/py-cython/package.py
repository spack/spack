from spack import *

class PyCython(Package):
    """The Cython compiler for writing C extensions for the Python language."""
    homepage = "https://pypi.python.org/pypi/cython"
    url      = "https://pypi.python.org/packages/source/C/Cython/Cython-0.21.2.tar.gz"

    version('0.21.2', 'd21adb870c75680dc857cd05d41046a4')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
