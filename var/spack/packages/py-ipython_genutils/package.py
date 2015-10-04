from spack import *

class PyIpythonGenutils(Package):
    """Vestigial utilities from IPython"""
    homepage = "http://ipython.org"
    version("0.1.0", "9a8afbe0978adbcbfcb3b35b2d015a56",
            url="https://pypi.python.org/packages/source/i/ipython_genutils/ipython_genutils-0.1.0.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
