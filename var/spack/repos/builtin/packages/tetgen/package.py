from spack import *

class Tetgen(Package):
    """TetGen is a program and library that can be used to generate tetrahedral
       meshes for given 3D polyhedral domains. TetGen generates exact constrained
       Delaunay tetrahedralizations, boundary conforming Delaunay meshes, and
       Voronoi paritions."""

    homepage = "http://www.tetgen.org"
    url      = "http://www.tetgen.org/files/tetgen1.4.3.tar.gz"

    version('1.4.3', 'd6a4bcdde2ac804f7ec66c29dcb63c18')

    # TODO: Make this a build dependency once build dependencies are supported
    # (see: https://github.com/LLNL/spack/pull/378).
    depends_on('cmake@2.8.7:', when='@1.5.0:')

    def install(self, spec, prefix):
        make('tetgen', 'tetlib')

        mkdirp(prefix.bin)
        install('tetgen', prefix.bin)

        mkdirp(prefix.include)
        install('tetgen.h', prefix.include)

        mkdirp(prefix.lib)
        install('libtet.a', prefix.lib)
