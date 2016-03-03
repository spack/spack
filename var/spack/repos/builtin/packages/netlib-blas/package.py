from spack import *
import os


class NetlibBlas(Package):
    """Netlib reference BLAS"""
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    variant('fpic', default=False, description="Build with -fpic compiler option")
    variant('fortran', default=False, description="Build with Fortran support")

    # virtual dependency
    provides('blas')

    # Doesn't always build correctly in parallel
    parallel = False

    def patch(self):
        os.symlink('make.inc.example', 'make.inc')

        mf = FileFilter('make.inc')
        if '+fortran' in spec:
            mf.filter('^FORTRAN.*', 'FORTRAN = f90')
            mf.filter('^LOADER.*',  'LOADER = f90')
        mf.filter('^CC =.*',  'CC = cc')

        if '+fpic' in self.spec:
            mf.filter('^OPTS.*=.*',  'OPTS = -O2 -frecursive -fpic')
            mf.filter('^CFLAGS =.*',  'CFLAGS = -O3 -fpic')


    def install(self, spec, prefix):
        make('blaslib')

        # Tests that blas builds correctly
        make('blas_testing')

        # No install provided
        mkdirp(prefix.lib)
        install('librefblas.a', prefix.lib)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('librefblas.a', 'blas.a')
            symlink('librefblas.a', 'libblas.a')
