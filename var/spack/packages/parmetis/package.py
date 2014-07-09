from spack import *

class Parmetis(Package):
    """ParMETIS is an MPI-based parallel library that implements a
       variety of algorithms for partitioning unstructured graphs,
       meshes, and for computing fill-reducing orderings of sparse
       matrices."""
    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview"
    url      = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz"

    versions = { '4.0.3' : 'f69c479586bf6bb7aff6a9bc0c739628', }

    depends_on('mpi')

    def install(self, spec, prefix):
        cmake(".",
              '-DGKLIB_PATH=%s/metis/GKlib' % pwd(),
              '-DMETIS_PATH=%s/metis' % pwd(),
              '-DSHARED=1',
              '-DCMAKE_C_COMPILER=mpicc',
              '-DCMAKE_CXX_COMPILER=mpicxx',
              '-DSHARED=1',
              *std_cmake_args)

        make()
        make("install")
