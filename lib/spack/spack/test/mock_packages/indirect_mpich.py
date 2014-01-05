from spack import *

class IndirectMpich(Package):
    """Test case for a package that depends on MPI and one of its
       dependencies requires a *particular version* of MPI.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/indirect_mpich-1.0.tar.gz"

    versions = { 1.0 : 'foobarbaz' }

    depends_on('mpi')
    depends_on('direct_mpich')

    def install(self, spec, prefix):
        pass
