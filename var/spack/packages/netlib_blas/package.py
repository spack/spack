from spack import *

class NetlibBlas(Package):
    """Netlib reference BLAS"""
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    # virtual dependency
    provides('blas')

    # Doesn't always build correctly in parallel
    parallel = False

    def install(self, spec, prefix):
        symlink('make.inc.example', 'make.inc')
        make('blaslib')
        
        # Tests that blas builds correctly
        make('blas_testing')

        # No install provided
        mkdirp(prefix.lib)
        install('librefblas.a', prefix.lib)

        # Blas virtual package should provide blas.a
        symlink(prefix.lib + '/librefblas.a', prefix.lib + '/blas.a')