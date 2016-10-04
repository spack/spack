##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class GribApi(Package):
    """The ECMWF GRIB API is an application program interface accessible from
       C, FORTRAN and Python programs developed for encoding and decoding WMO
       FM-92 GRIB edition 1 and edition 2 messages."""

    homepage = "https://software.ecmwf.int/wiki/display/GRIB/Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.17.0-Source.tar.gz"

    version('1.17.0', 'bca7114d2c3100501a08190a146818d2')
    version('1.16.0', '8c7fdee03344e4379d400ae20976a460')

    variant('netcdf', default=False, description='Enable netcdf encoding/decoding using netcdf library')
    variant('jpeg', default=True, description='Enable jpeg 2000 for grib 2 decoding/encoding')
    variant('png', default=False, description='Enable png for decoding/encoding')

    depends_on('cmake', type='build')
    depends_on('libpng', when='+png')
    depends_on('netcdf', when='+netcdf')
    depends_on('jasper', when='+jpeg')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.append('-DBUILD_SHARED_LIBS=BOTH')

        # We will add python support later.
        options.append('-DENABLE_PYTHON=OFF')

        # Disable FORTRAN interface if we don't have it.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            options.append('-DENABLE_FORTRAN=OFF')

        if '+netcdf' in spec:
            options.append('-DENABLE_NETCDF=ON')
            options.append('-DNETCDF_PATH=%s' % spec['netcdf'].prefix)
        else:
            options.append('-DENABLE_NETCDF=OFF')

        if '+jpeg' in spec:
            options.append('-DENABLE_JPG=ON')
            options.append('-DJASPER_PATH=%s' % spec['jasper'].prefix)
        else:
            options.append('-DENABLE_JPG=OFF')

        if '+png' in spec:
            options.append('-DENABLE_PNG=ON')
        else:
            options.append('-DENABLE_PNG=OFF')

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
