from spack import *

class Qrupdate(Package):
    """qrupdate is a Fortran library for fast updates of QR and
    Cholesky decompositions."""

    homepage = "http://sourceforge.net/projects/qrupdate/"
    url      = "https://downloads.sourceforge.net/qrupdate/qrupdate-1.1.2.tar.gz"

    version('1.1.2', '6d073887c6e858c24aeda5b54c57a8c4')

    depends_on("blas")
    depends_on("lapack")

    def install(self, spec, prefix):
        # Build static and dynamic libraries
        make("lib", "solib")
        make("install", "PREFIX=%s" % prefix)
