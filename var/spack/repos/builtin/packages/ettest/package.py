from spack import *
import llnl.util.tty as tty
import os

class Ettest(CMakePackage):
    """Get stack trace EVERY time a program exits."""

    homepage = "https://github.com/citibeth/ettest"
    version('develop', git='https://github.com/citibeth/ettest.git', branch='develop')

    maintainers = ['citibeth']

    depends_on('cmake')
    depends_on('everytrace+mpi+fortran')

    # Currently the only MPI this everytrace works with.
    depends_on('openmpi')

    def configure_args(self):
        return []

    def setup_environment(self, spack_env, env):
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
