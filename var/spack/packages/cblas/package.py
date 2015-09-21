from spack import *
import os

class Cblas(Package):
    """The BLAS (Basic Linear Algebra Subprograms) are routines that
       provide standard building blocks for performing basic vector and
       matrix operations."""

    homepage = "http://www.netlib.org/blas/_cblas/"

    # tarball has no version, but on the date below, this MD5 was correct.
    version('2015-06-06', '1e8830f622d2112239a4a8a83b84209a',
            url='http://www.netlib.org/blas/blast-forum/cblas.tgz')

    depends_on('blas')
    parallel = False

    def patch(self):
        mf = FileFilter('Makefile.in')

        mf.filter('^BLLIB =.*', 'BLLIB = %s/libblas.a' % self.spec['blas'].prefix.lib)
        mf.filter('^CC =.*', 'CC = cc')
        mf.filter('^FC =.*', 'FC = f90')


    def install(self, spec, prefix):
        make('all')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        # Rename the generated lib file to libcblas.a
        install('./lib/cblas_LINUX.a', '%s/libcblas.a' % prefix.lib)
        install('./include/cblas.h','%s' % prefix.include)
        install('./include/cblas_f77.h','%s' % prefix.include)

