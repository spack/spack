# Install with:
#      spack diy --skip-patch everytrace@devel +fortran +mpi ^openmpi

from spack import *
import llnl.util.tty as tty
import os

class Everytrace(CMakePackage):
    """Get stack trace EVERY time a program exits."""

    homepage = "https://github.com/citibeth/everytrace"
    url          = "https://github.com/citibeth/everytrace/tarball/0.2.0"

    version('0.2.0', '2af0e5b6255064d5191accebaa70d222')
    version('develop', git='https://github.com/citibeth/everytrace.git', branch='develop', preferred=True)

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('fortran', default=True, description='Enable use with Fortran programs')

    depends_on('mpi', when='+mpi')
    depends_on('cmake')

    def configure_args(self):
        spec = self.spec
        return [
            '-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_FORTRAN=%s' % ('YES' if '+fortran' in spec else 'NO')]

    def setup_environment(self, spack_env, env):
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
