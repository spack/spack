from spack import *
import os

class SuiteSparse(Package):
    """
    SuiteSparse is a suite of sparse matrix algorithms
    """
    homepage = 'http://faculty.cse.tamu.edu/davis/suitesparse.html'
    url = 'http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-4.5.1.tar.gz'

    version('4.5.1', 'f0ea9aad8d2d1ffec66a5b6bfeff5319')

    # FIXME: (see below)
    # variant('tbb', default=True, description='Build with Intel TBB')
    variant('fpic', default=True, description='Build position independent code (required to link with shared libraries)')

    depends_on('blas')
    depends_on('lapack')

    depends_on('metis@5.1.0', when='@4.5.1')
    # FIXME:
    # in @4.5.1. TBB support in SPQR seems to be broken as TBB-related linkng flags
    # does not seem to be used, which leads to linking errors on Linux.
    # Try re-enabling in future versions.
    # depends_on('tbb', when='+tbb')

    def install(self, spec, prefix):
        # The build system of SuiteSparse is quite old-fashioned
        # It's basically a plain Makefile which include an header (SuiteSparse_config/SuiteSparse_config.mk)
        # with a lot of convoluted logic in it.
        # Any kind of customization will need to go through filtering of that file

        make_args = ['INSTALL=%s' % prefix]

        # inject Spack compiler wrappers
        make_args.extend([
             'AUTOCC=no',
             'CC=cc',
             'CXX=c++',
             'F77=f77'
        ])
        if '+fpic' in spec:
            make_args.extend(['CFLAGS=-fPIC', 'FFLAGS=-fPIC'])

        # use Spack's metis in CHOLMOD/Partition module,
        # otherwise internal Metis will be compiled
        make_args.extend([
             'MY_METIS_LIB=-L%s -lmetis' % spec['metis'].prefix.lib,
             'MY_METIS_INC=%s' % spec['metis'].prefix.include,
        ])

        # Intel TBB in SuiteSparseQR
        if '+tbb' in spec:
            make_args.extend([
                'SPQR_CONFIG=-DHAVE_TBB',
                'TBB=-L%s -ltbb' % spec['tbb'].prefix.lib,
            ])

        # --------------- Locate BLAS and LAPACK
        exts = ['.a', '.so']
        if ('+shared' in spec) or ('+fpic' in spec):
            exts.reverse()

        # Find BLAS for the not-so-powerful makefile
        blas_lib = None
        for ext in exts:
            blas_lib = os.path.join(spec['blas'].prefix, 'lib', 'libblas' + ext)
            if os.path.exists(blas_lib):
                break
        if blas_lib is None:
            tty.error('Cannot find libblas in path %s')


        # Find LAPACK for the not-so-powerful makefile
        lapack_lib = None
        for ext in exts:
            lapack_lib = os.path.join(spec['lapack'].prefix, 'lib', 'liblapack' + ext)
            if os.path.exists(lapack_lib):
                break
        if lapack_lib is None:
            tty.error('Cannot find liblapack in path %s')
        # ---------------------------------------------

        # BLAS arguments require path to libraries
        # FIXME : (blas / lapack always provide libblas and liblapack as aliases)
        make_args.extend([
            'BLAS=%s' % blas_lib,
            'LAPACK=%s' % lapack_lib
        ])

        make('install', *make_args)
