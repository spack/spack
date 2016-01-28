from spack import *

class Caliper(Package):
    """
    Caliper is a generic context annotation system. It gives programmers the
    ability to provide arbitrary program context information to (performance)
    tools at runtime.
    """

    homepage = "https://github.com/LLNL/Caliper"
    url      = ""

    version('master', git='ssh://git@cz-stash.llnl.gov:7999/piper/caliper.git')

    variant('mpi', default=False, description='Enable MPI function wrappers.')

    depends_on('libunwind')
    depends_on('papi')
    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):
      with working_dir('build', create=True):
        cmake('..', *std_cmake_args)
        make()
        make("install")
