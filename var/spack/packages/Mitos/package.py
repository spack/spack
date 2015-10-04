from spack import *

class Mitos(Package):
    """Mitos is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/scalability-llnl/Mitos"
    url      = "https://github.com/scalability-llnl/Mitos"

    version('0.9.1', 'c6cb57f3cae54f5157affd97ef7ef79e', git='https://github.com/scalability-llnl/Mitos.git', tag='v0.9.1')

    depends_on('dyninst@8.2.1:')
    depends_on('hwloc')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
