##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
