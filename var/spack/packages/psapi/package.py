from spack import *

class Psapi(Package):
    """PSAPI is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/scalability-llnl/PSAPI"
    url      = "http://www.example.com/memaxes-psapi-1.0.tar.gz"

    version('0.5', git='https://github.com/scalability-llnl/PSAPI.git', tag='v0.5')

    depends_on('dyninst')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
