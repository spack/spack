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


class Libemos(CMakePackage):
    """The Interpolation library (EMOSLIB) includes Interpolation software and
       BUFR & CREX encoding/decoding routines."""

    homepage = "https://software.ecmwf.int/wiki/display/EMOS/Emoslib"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473472/libemos-4.4.2-Source.tar.gz"

    version('4.4.7', '395dcf21cf06872f772fb6b73d8e67b9')
    version('4.4.2', 'f15a9aff0f40861f3f046c9088197376')

    variant('eccodes', default=False,
            description="Use eccodes instead of grib-api for GRIB decoding")
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('eccodes', when='+eccodes')
    depends_on('grib-api', when='~eccodes')
    depends_on('fftw+float+double')
    depends_on('cmake@2.8.11:', type='build')

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('+eccodes'):
            args.append('-DENABLE_ECCODES=ON')
            args.append('-DECCODES_PATH=%s' % spec['eccodes'].prefix)
        else:
            args.append('-DENABLE_ECCODES=OFF')
            args.append('-DGRIB_API_PATH=%s' % spec['grib-api'].prefix)

        # To support long pathnames that spack generates
        args.append('-DCMAKE_Fortran_FLAGS=-ffree-line-length-none')

        return args
