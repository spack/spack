from spack import *

class Pidx(Package):
    """PIDX Parallel I/O Library"""

    homepage = "http://www.cedmav.com/pidx"
    #url      = "http://www.example.com/pidx-1.0.tar.gz"

    version('1.0', git='https://github.com/sci-visus/PIDX.git',
            commit='6afa1cf71d1c41263296dc049c8fabaf73c296da')

    depends_on("mpi")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
