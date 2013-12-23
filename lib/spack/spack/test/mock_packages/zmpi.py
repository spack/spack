from spack import *

class Zmpi(Package):
    """This is a fake MPI package used to demonstrate virtual package providers
       with dependencies."""
    homepage = "http://www.spack-fake-zmpi.org"
    url      = "http://www.spack-fake-zmpi.org/downloads/zmpi-1.0.tar.gz"

    versions = { '1.0' : 'foobarbaz' }

    provides('mpi@:10.0')
    depends_on('fake')

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
