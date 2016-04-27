from spack import *


class SuiteSparse(Package):
    """
    SuiteSparse is a suite of sparse matrix algorithms
    """
    homepage = 'http://faculty.cse.tamu.edu/davis/suitesparse.html'
    url = 'http://faculty.cse.tamu.edu/davis/SuiteSparse/SuiteSparse-4.5.1.tar.gz'

    version('4.5.1', 'f0ea9aad8d2d1ffec66a5b6bfeff5319')

    # FIXME: (see below)
    # variant('tbb', default=True, description='Build with Intel TBB')

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
             'F77=f77',
        ])

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

        # BLAS arguments require path to libraries
        # FIXME : (blas / lapack always provide libblas and liblapack as aliases)
        make_args.extend([
            'BLAS=-lblas',
            'LAPACK=-llapack'
        ])

        make('install', *make_args)
