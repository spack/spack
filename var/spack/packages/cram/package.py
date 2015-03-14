from spack import *

class Cram(Package):
    """Cram runs many small MPI jobs inside one large MPI job."""
    homepage = "https://github.com/scalability-llnl/cram"
    url      = "http://github.com/scalability-llnl/cram/archive/v1.0.1.tar.gz"

    version('1.0.1', 'c73711e945cf5dc603e44395f6647f5e')

    depends_on("mpi")

    def install(self, spec, prefix):
        cmake(".", *std_cmake_args)
        make()
        make("install")
