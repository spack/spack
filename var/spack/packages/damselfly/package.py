from spack import *

class Damselfly(Package):
    """Damselfly is a model-based parallel network simulator."""
    homepage = "https://github.com/llnl/damselfly"
    url      = "https://github.com/llnl/damselfly"

    version('1.0', '05cf7e2d8ece4408c0f2abb7ab63fd74c0d62895', git='https://github.com/llnl/damselfly.git', tag='v1.0')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
	    cmake('-DCMAKE_BUILD_TYPE=release', '..', *std_cmake_args)
	    make()
	    make('install')
