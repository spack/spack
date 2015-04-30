from spack import *

class Mitos(Package):
    """Mitos is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/scalability-llnl/Mitos"
    url      = "https://github.com/scalability-llnl/Mitos"

    version('0.7', '319ece59d6794cccb66bfcc0abfec661', git='https://github.com/scalability-llnl/Mitos.git', tag='v0.7')

    depends_on('dyninst')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
