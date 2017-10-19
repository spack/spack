##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class GribApi(CMakePackage):
    """The ECMWF GRIB API is an application program interface accessible from
       C, FORTRAN and Python programs developed for encoding and decoding WMO
       FM-92 GRIB edition 1 and edition 2 messages."""

    homepage = "https://software.ecmwf.int/wiki/display/GRIB/Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.17.0-Source.tar.gz"

    version('1.21.0', 'eb64c5eb72e6e90841237cba9d644016')
    version('1.17.0', 'bca7114d2c3100501a08190a146818d2')
    version('1.16.0', '8c7fdee03344e4379d400ae20976a460')

    variant('netcdf', default=False, description='Enable netcdf encoding/decoding using netcdf library')
    variant('jpeg', default=True, description='Enable jpeg 2000 for grib 2 decoding/encoding')
    variant('png', default=False, description='Enable png for decoding/encoding')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('libpng', when='+png')
    depends_on('netcdf', when='+netcdf')
    depends_on('jasper', when='+jpeg')
    depends_on('cmake@2.8.11:', type='build')

    def cmake_args(self):
        spec = self.spec
        args = ['-DBUILD_SHARED_LIBS=BOTH']

        # We will add python support later.
        args.append('-DENABLE_PYTHON=OFF')

        # Disable FORTRAN interface if we don't have it.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            args.append('-DENABLE_FORTRAN=OFF')

        if '+netcdf' in spec:
            args.append('-DENABLE_NETCDF=ON')
            args.append('-DNETCDF_PATH=%s' % spec['netcdf'].prefix)
        else:
            args.append('-DENABLE_NETCDF=OFF')

        if '+jpeg' in spec:
            args.append('-DENABLE_JPG=ON')
            args.append('-DJASPER_PATH=%s' % spec['jasper'].prefix)
        else:
            args.append('-DENABLE_JPG=OFF')

        if '+png' in spec:
            args.append('-DENABLE_PNG=ON')
        else:
            args.append('-DENABLE_PNG=OFF')

        return args
