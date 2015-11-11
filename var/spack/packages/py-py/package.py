from spack import *

class PyPy(Package):
    """library with cross-python path, ini-parsing, io, code, log facilities"""
    homepage = "http://pylib.readthedocs.org/"
    version("1.4.26", "30c3fd92a53f1a5ed6f3591c1fe75c0e",
            url="https://pypi.python.org/packages/source/p/py/py-1.4.26.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
