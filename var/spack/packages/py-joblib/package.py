from spack import *

class PyJoblib(Package):
    """Lightweight pipelining: using Python functions as pipeline jobs."""
    homepage = "http://packages.python.org/joblib/"
    version("0.8.4", "90a1c25cc4dc4a8e3536093dbc35cff3",
            url="https://pypi.python.org/packages/source/j/joblib/joblib-0.8.4.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
