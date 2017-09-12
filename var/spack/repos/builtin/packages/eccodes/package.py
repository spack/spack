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
#
from spack import *


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = "https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2"
    list_url = "https://software.ecmwf.int/wiki/display/ECC/Releases"

    version('2.2.0', 'b27e6f0a3eea5b92dac37372e4c45a62')

    variant('netcdf', default=True,
            description="Support GRIB to NetCDF conversion")
    variant('jpeg', default=True,
            description="Support JPEG2000 encoding/decoding")
    variant('png', default=True,
            description="Support PNG encoding/decoding")
    variant('python', default=False,
            description="Build the eccodes Python interface")
    variant('pthreads', default=False,
            description="Enable POSIX threads")
    variant('openmp', default=False,
            description="Enable OpenMP threads")
    variant('memfs', default=False,
            description="Memory based access to definitions/samples")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('netcdf', when='+netcdf')
    depends_on('openjpeg', when='+jpeg')
    depends_on('libpng', when='+png')
    depends_on('py-numpy', when='+python')
    extends('python', when='+python')

    def cmake_args(self):
        variants = ['+netcdf', '+jpeg', '+png', '+python',
                    '+pthreads', '+openmp', '+memfs']
        options = ['NETCDF', 'JPG', 'PNG', 'PYTHON',
                   'ECCODES_THREADS', 'ECCODES_OMP_THREADS', 'MEMFS']
        return map(lambda variant, option: "-DENABLE_%s=%s" %
                   (option, 'YES' if variant in self.spec else 'NO'),
                   variants, options)
