import os
from spack import *

class Tetgen(Package):
    """TetGen is a program and library that can be used to generate tetrahedral
       meshes for given 3D polyhedral domains. TetGen generates exact constrained
       Delaunay tetrahedralizations, boundary conforming Delaunay meshes, and
       Voronoi paritions."""

    homepage = "http://www.tetgen.org"
    url      = "http://www.tetgen.org/files/tetgen1.4.3.zip"

    version('1.5.0', '3891aca3a59872048ead2f217d723131', mirror_only=True)
    version('1.4.3', '7d01fde9e4b9176ebb706c549e01cd04')

    # TODO: Make this a build dependency once build dependencies are supported
    # (see: https://github.com/LLNL/spack/pull/378).
    depends_on('cmake@2.8.7:', when='@1.5.0:')

    def install(self, spec, prefix):
        if spec.satisfies('@1.5.0:'):
            cmake('.')
        else:
            cd('tetgen%s' % self.version)

        make('tetgen', 'tetlib')

        mkdirp(prefix.bin)
        install('tetgen', prefix.bin)

        mkdirp(prefix.include)
        install('tetgen.h', prefix.include)

        mkdirp(prefix.lib)
        install('libtet.a', prefix.lib)
