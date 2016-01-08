from spack import *

class PyCython(Package):
    """The Cython compiler for writing C extensions for the Python language."""
    homepage = "http://www.cython.org"
    version("0.21.2", "d21adb870c75680dc857cd05d41046a4",
            url="https://pypi.python.org/packages/source/C/Cython/Cython-0.21.2.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
