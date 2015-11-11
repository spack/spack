from spack import *

class PyTables(Package):
    """Hierarchical datasets for Python"""
    homepage = "http://www.pytables.org/"
    version("3.1.1", "38d917f0c6dfb0bc28ce9ea0c3492524",
            url="https://pypi.python.org/packages/source/t/tables/tables-3.1.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
