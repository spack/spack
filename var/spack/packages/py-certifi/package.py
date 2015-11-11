from spack import *

class PyCertifi(Package):
    """Python package for providing Mozilla's CA Bundle."""
    homepage = "http://python-requests.org"
    version("14.05.14", "315ea4e50673a16ab047099f816fd32a",
            url="https://pypi.python.org/packages/source/c/certifi/certifi-14.05.14.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
