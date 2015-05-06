from spack import *
from subprocess import call

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
	# CMake could possibly be used if build gets more complex

	# TODO: Run blas tests after building
	call(['cp', 'make.inc.example', 'make.inc'])
        make('blaslib')
	mkdirp(prefix.lib)
	install('librefblas.a', prefix.lib)

	# blas needs to be named blas.a to provide blas interface
	call(['ln', '-s', prefix.lib + '/librefblas.a', prefix.lib + '/blas.a'])
