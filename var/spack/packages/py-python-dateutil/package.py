from spack import *

class PyPythonDateutil(Package):
    """Extensions to the standard Python datetime module"""
    homepage = "http://labix.org/python-dateutil"
    version("2.2", "c1f654d0ff7e33999380a8ba9783fd5c",
            url="https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-2.2.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
