from spack import *

class Cnmem(Package):
    """RAJA Parallel Framework."""
    homepage = "https://github.com/NVIDIA/cnmem"

    version('git', git='https://github.com/NVIDIA/cnmem.git', branch="master")

    def install(self, spec, prefix):
            cmake('.',*std_cmake_args)
            make()
            make('install')
