##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#
from spack import *


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = "https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2"
    list_url = "https://software.ecmwf.int/wiki/display/ECC/Releases"

    version('2.5.0', '5a7e92c58418d855082fa573efd352aa')
    version('2.2.0', 'b27e6f0a3eea5b92dac37372e4c45a62')

    variant('netcdf', default=False,
            description='Enable GRIB to NetCDF conversion tool')
    variant('jp2k', default='openjpeg', values=('openjpeg', 'jasper', 'none'),
            description='Specify JPEG2000 decoding/encoding backend')
    variant('png', default=False,
            description='Enable PNG support for decoding/encoding')
    variant('aec', default=False,
            description='Enable Adaptive Entropy Coding for decoding/encoding')
    variant('pthreads', default=False,
            description='Enable POSIX threads')
    variant('openmp', default=False,
            description='Enable OpenMP threads')
    variant('memfs', default=False,
            description='Enable memory based access to definitions/samples')
    variant('python', default=False,
            description='Enable the Python interface')
    variant('fortran', default=True, description='Enable the Fortran support')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('netcdf', when='+netcdf')
    depends_on('openjpeg', when='jp2k=openjpeg')
    depends_on('jasper', when='jp2k=jasper')
    depends_on('libpng', when='+png')
    depends_on('libaec', when='+aec')
    depends_on('python@:2', when='+python')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    extends('python', when='+python')

    conflicts('+openmp', when='+pthreads',
              msg='Cannot enable both POSIX threads and OMP')

    # The following enforces linking against the specified JPEG2000 backend.
    patch('enable_only_openjpeg.patch', when='jp2k=openjpeg')
    patch('enable_only_jasper.patch', when='jp2k=jasper')

    def cmake_args(self):
        variants = ['+netcdf', '+png', '+aec', '+pthreads',
                    '+openmp', '+memfs', '+python', '+fortran']
        options = ['NETCDF', 'PNG', 'AEC', 'ECCODES_THREADS',
                   'ECCODES_OMP_THREADS', 'MEMFS', 'PYTHON', 'FORTRAN']

        args = map(lambda var, opt:
                   "-DENABLE_%s=%s" %
                   (opt, 'ON' if var in self.spec else 'OFF'),
                   variants,
                   options)

        if self.spec.variants['jp2k'].value == 'none':
            args.append('-DENABLE_JPG=OFF')
        else:
            args.append('-DENABLE_JPG=ON')

        return args
