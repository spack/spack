from spack import *

class PyStatsmodels(Package):
    """Statistical computations and models for use with SciPy"""
    homepage = "http://statsmodels.sourceforge.net/"
    version("0.6.1", "f7580ebf7d2a2c9b87abfad190dcb9a3",
            url="https://pypi.python.org/packages/source/s/statsmodels/statsmodels-0.6.1.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
