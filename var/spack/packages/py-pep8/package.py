from spack import *

class PyPep8(Package):
    """Python style guide checker"""
    homepage = "http://pep8.readthedocs.org/"
    version("1.6.1", "76cf60b245f8549cb458ffcd85710738",
            url="https://pypi.python.org/packages/source/p/pep8/pep8-1.6.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
