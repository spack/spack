from spack import *

class PyMock(Package):
    """A Python Mocking and Patching Library for Testing"""
    homepage = "http://www.voidspace.org.uk/python/mock/"
    version("1.0.1", "c3971991738caa55ec7c356bbc154ee2",
            url="https://pypi.python.org/packages/source/m/mock/mock-1.0.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
