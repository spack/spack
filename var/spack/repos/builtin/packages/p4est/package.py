from spack import *

class P4est(Package):
    """Dynamic management of a collection (a forest) of adaptive octrees in parallel"""
    homepage = "http://www.p4est.org"
    url      = "http://p4est.github.io/release/p4est-1.1.tar.gz"

    version('1.1', '37ba7f4410958cfb38a2140339dbf64f')

    # build dependencies
    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool@2.4.2:')

    # other dependencies
    depends_on('lua') # Needed for the submodule sc
    depends_on('mpi')
    depends_on('zlib')

    def install(self, spec, prefix):
        options = ['--enable-mpi',
                   '--enable-shared',
                   '--disable-vtk-binary',
                   '--without-blas',
                   'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
                   'CFLAGS=-O2',
                   'CC=%s'  % self.spec['mpi'].mpicc,
                   'CXX=%s' % self.spec['mpi'].mpicxx,
                   'FC=%s'  % self.spec['mpi'].mpifc,
                   'F77=%s' % self.spec['mpi'].mpif77
                  ]

        configure('--prefix=%s' % prefix, *options)

        make()
        make("check")
        make("install")
