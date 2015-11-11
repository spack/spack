from spack import *

class PyPickleshare(Package):
    """Tiny 'shelve'-like database with concurrency support"""
    homepage = "https://github.com/vivainio/pickleshare"
    version("0.5", "25337740507cb855ad58bfcf60f7710e",
            url="https://pypi.python.org/packages/source/p/pickleshare/pickleshare-0.5.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
