from spack import *

class PyPytest(Package):
    """pytest: simple powerful testing with Python"""
    homepage = "http://pytest.org"
    version("2.6.4", "14341e122f7e9031a0948eb6b01a2640",
            url="https://pypi.python.org/packages/source/p/pytest/pytest-2.6.4.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
