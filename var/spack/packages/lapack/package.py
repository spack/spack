# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install lapack
#
# You can always get back here to change things with:
#
#     spack edit lapack
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Lapack(Package):
    """
    LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least
    squared solutions to linear sets of equations, eigenvector
    analysis, singular value decomposition, etc. It is a very
    comprehensive and reputable package that has found extensive
    use in the scientific community.
    """
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    depends_on('atlas')

    def install(self, spec, prefix):
        cmake(".", '-DBLAS_LIBRARIES=f77blas;atlas', *std_cmake_args)

        make()
        make("install")
