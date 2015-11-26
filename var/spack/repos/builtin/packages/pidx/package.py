from spack import *

class Pidx(Package):
    """PIDX Parallel I/O Library.

    PIDX is an efficient parallel I/O library that reads and writes
    multiresolution IDX data files.
    """

    homepage = "http://www.cedmav.com/pidx"

    version('1.0', git='https://github.com/sci-visus/PIDX.git',
            commit='6afa1cf71d1c41263296dc049c8fabaf73c296da')

    depends_on("mpi")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
