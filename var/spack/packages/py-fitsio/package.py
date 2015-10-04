from spack import *

class PyFitsio(Package):
    """A full featured python library to read from and write to FITS files."""
    homepage = "https://github.com/esheldon/fitsio"
    version("0.9.7", "75fa05f999ae8f55c8290bd78ada49e7",
            url="https://pypi.python.org/packages/source/f/fitsio/fitsio-0.9.7.tar.gz")

    extends("python")
    depends_on("py-numpy")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
