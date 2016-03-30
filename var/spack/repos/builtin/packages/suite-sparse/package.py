from spack import *


class SuiteSparse(Package):
    """
    SuiteSparse is a suite of sparse matrix algorithms
    """
    homepage = 'http://faculty.cse.tamu.edu/davis/suitesparse.html'
    url = 'http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-4.5.1.tar.gz'

    version('4.5.1', 'f0ea9aad8d2d1ffec66a5b6bfeff5319')

    depends_on('blas')
    depends_on('lapack')

    depends_on('metis@5.1.0', when='@4.5.1')

    def install(self, spec, prefix):
        # The build system of SuiteSparse is quite old-fashioned
        # It's basically a plain Makefile which include an header (SuiteSparse_config/SuiteSparse_config.mk)
        # with a lot of convoluted logic in it.
        # Any kind of customization will need to go through filtering of that file

        # FIXME : this actually uses the current workaround
        # FIXME : (blas / lapack always provide libblas and liblapack as aliases)
        make('install', 'INSTALL=%s' % prefix,

             # inject Spack compiler wrappers
             'AUTOCC=no',
             'CC=cc',
             'CXX=c++',
             'F77=f77',

             # BLAS arguments require path to libraries
             'BLAS=-lblas',
             'LAPACK=-llapack')
