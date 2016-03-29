from spack import *

class P4est(Package):
    """Dynamic management of a collection (a forest) of adaptive octrees in parallel"""
    homepage = "http://www.p4est.org"
    url      = "http://p4est.github.io/release/p4est-1.1.tar.gz"

    version('1.1', '37ba7f4410958cfb38a2140339dbf64f')

    # disable by default to make it work on frontend of clusters
    variant('tests', default=False, description='Run small tests')

    depends_on('mpi')

    def install(self, spec, prefix):
        options = ['--enable-mpi',
                   '--enable-shared',
                   '--disable-vtk-binary',
                   '--without-blas',
                   'CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL',
                   'CFLAGS=-O2',
                   'CC=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpicc'), # TODO: use ENV variables or MPI class wrappers
                   'CXX=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpic++'),
                   'FC=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpif90'),
                   'F77=%s' % join_path(self.spec['mpi'].prefix.bin, 'mpif77'),
                  ]

        configure('--prefix=%s' % prefix, *options)

        make()
        if '+tests' in self.spec:
            make("check")

        make("install")
