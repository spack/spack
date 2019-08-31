# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mapnik(AutotoolsPackage):
    """
    Mapnik combines pixel-perfect image output with lightning-fast cartographic
    algorithms, and exposes interfaces in C++, Python, and Node.
    """

    homepage = "https://mapnik.org/"
    url      = "https://github.com/mapnik/mapnik/releases/download/v3.0.22/mapnik-v3.0.22.tar.bz2"

    version('3.0.22', sha256='930612ad9e604b6a29b9cea1bc1de85cf7cf2b2b8211f57ec8b6b94463128ab9')

    depends_on('python', type=('build', 'run'))
    # Build fails with boost@1.70
    depends_on('boost@:1.69.0+filesystem+system+icu+program_options cxxstd=11')
    depends_on('icu4c')
    depends_on('zlib')
    depends_on('freetype')
    depends_on('libxml2')
    depends_on('harfbuzz')
    depends_on('libpng')
    depends_on('libjpeg')
    depends_on('libtiff')
    depends_on('proj')
    depends_on('cairo')
    depends_on('postgresql')
    depends_on('gdal')
    depends_on('sqlite+rtree')
    depends_on('libwebp')

    # Build fails for gcc@9
    conflicts('%gcc@9.0.0:')

    def configure_args(self):
        args = []
        args.append('CXXFLAGS="-std=c++11"')
        # config is expecting PREFIX not "prefix"
        args.append('PREFIX=' + str(self.prefix))
        return args
