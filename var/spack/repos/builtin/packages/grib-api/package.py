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
    """The ECMWF GRIB API is an application program interface accessible from C,
       FORTRAN and Python programs developed for encoding and decoding WMO
       FM-92 GRIB edition 1 and edition 2 messages."""

    homepage = "https://software.ecmwf.int/wiki/display/GRIB/Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.17.0-Source.tar.gz?api=v2"

    version('1.17.0', 'bca7114d2c3100501a08190a146818d2')

    depends_on('netcdf')
    depends_on('jasper')

    def install(self, spec, prefix):
        configure_options = [
            '--prefix={0}'.format(prefix),
            '--with-netcdf={0}'.format(spec['netcdf'].prefix),
            '--with-jasper={0}'.format(spec['jasper'].prefix)
        ]
        configure(*configure_options)

        make()
        make('install')
