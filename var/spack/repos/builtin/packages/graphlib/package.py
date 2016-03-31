from spack import *

class Graphlib(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    homepage = "http://https://github.com/lee218llnl/graphlib"
    url      = "https://github.com/lee218llnl/graphlib/archive/v2.0.0.tar.gz"

    version('2.0.0', '43c6df84f1d38ba5a5dce0ae19371a70')

    def install(self, spec, prefix):
        which('cmake')(".", *std_cmake_args)

        make()
        make("install")
