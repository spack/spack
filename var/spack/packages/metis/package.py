from spack import *

class Metis(Package):
    """METIS is a set of serial programs for partitioning graphs,
       partitioning finite element meshes, and producing fill reducing
       orderings for sparse matrices. The algorithms implemented in
       METIS are based on the multilevel recursive-bisection,
       multilevel k-way, and multi-constraint partitioning schemes."""

    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    url      = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe')

    depends_on('mpi')

    def install(self, spec, prefix):
        cmake(".",
              '-DGKLIB_PATH=%s/GKlib' % pwd(),
              '-DSHARED=1',
              '-DCMAKE_C_COMPILER=mpicc',
              '-DCMAKE_CXX_COMPILER=mpicxx',
              '-DSHARED=1',
              *std_cmake_args)

        make()
        make("install")
