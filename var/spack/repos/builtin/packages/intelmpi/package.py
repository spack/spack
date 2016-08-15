from spack import *

class Intelmpi(Package):
    """Intel MPI"""

    homepage = "http://www.example.com"
    url      = "https://software.intel.com/en-us/intel-mpi-library"

    version('4.1.0')

    # Provides a virtual dependency 'mpi'
    provides('mpi')

#    def install(self, spec, prefix):
#        configure("--prefix=%s" % prefix)
#        make()
#        make("install")
