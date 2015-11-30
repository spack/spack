from spack import *

class Mitos(Package):
    """Mitos is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/scalability-llnl/Mitos"
    url      = "https://github.com/scalability-llnl/Mitos"

    version('0.9.2',
            git='https://github.com/scalability-llnl/Mitos.git',
            commit='8cb143a2e8c00353ff531a781a9ca0992b0aaa3d')

    version('0.9.1',
            git='https://github.com/scalability-llnl/Mitos.git',
            tag='v0.9.1')

    depends_on('dyninst@8.2.1:')
    depends_on('hwloc')
    depends_on('mpi')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
