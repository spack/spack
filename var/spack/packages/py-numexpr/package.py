from spack import *

class PyNumexpr(Package):
    """Fast numerical expression evaluator for NumPy"""
    homepage = "https://github.com/pydata/numexpr"
    version("2.4", "df7e8d9e9dbb145b56d43c465c2bf854",
            url="https://pypi.python.org/packages/source/n/numexpr/numexpr-2.4.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
