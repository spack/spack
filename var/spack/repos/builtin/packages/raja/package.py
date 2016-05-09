from spack import *

class Raja(Package):
    """RAJA Parallel Framework."""
    homepage = "http://software.llnl.gov/RAJA/"

    version('git', git='https://github.com/LLNL/RAJA.git', branch="master")

    def install(self, spec, prefix):
            cmake('.',*std_cmake_args)
            make()
            make('install')
