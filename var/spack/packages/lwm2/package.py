from spack import *

class Lwm2(Package):
    """LWM2: Light Weight Measurement Module.  This is a PMPI module
       that can collect a number of time-sliced MPI and POSIX I/O
       measurements from a program.
    """
    homepage = "https://jay.grs.rwth-aachen.de/redmine/projects/lwm2"

    version('torus', hg='https://jay.grs.rwth-aachen.de/hg/lwm2', branch='torus')

    depends_on("papi")
    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
