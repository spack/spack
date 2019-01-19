# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgeotiff(AutotoolsPackage):
    """GeoTIFF represents an effort by over 160 different remote sensing, GIS,
    cartographic, and surveying related companies and organizations to
    establish a TIFF based interchange format for georeferenced raster imagery.
    """

    homepage = "https://trac.osgeo.org/geotiff/"
    url      = "http://download.osgeo.org/geotiff/libgeotiff/libgeotiff-1.4.2.tar.gz"

    version('1.4.2', '96ab80e0d4eff7820579957245d844f8')

    variant('zlib', default=True, description='Include zlib support')
    variant('jpeg', default=True, description='Include jpeg support')
    variant('proj', default=True, description='Use PROJ.4 library')

    depends_on('zlib', when='+zlib')
    depends_on('jpeg', when='+jpeg')
    depends_on('libtiff')
    depends_on('proj', when='+proj')

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-libtiff={0}'.format(spec['libtiff'].prefix),
        ]

        if '+zlib' in spec:
            args.append('--with-zlib={0}'.format(spec['zlib'].prefix))
        else:
            args.append('--with-zlib=no')

        if '+jpeg' in spec:
            args.append('--with-jpeg={0}'.format(spec['jpeg'].prefix))
        else:
            args.append('--with-jpeg=no')

        if '+proj' in spec:
            args.append('--with-proj={0}'.format(spec['proj'].prefix))
        else:
            args.append('--with-proj=no')

        return args
