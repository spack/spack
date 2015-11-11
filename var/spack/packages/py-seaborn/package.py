from spack import *

class PySeaborn(Package):
    """Seaborn: statistical data visualization"""
    homepage = "http://stanford.edu/~mwaskom/software/seaborn/"
    version("0.5.1", "2ce6ea7d3c67858c0b1f5793fa2043b8",
            url="https://pypi.python.org/packages/source/s/seaborn/seaborn-0.5.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
