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
#
from spack import *


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF which provides an application
    programming interface and a set of tools for decoding and encoding
    messages in the following formats:

      WMO FM-92 GRIB edition 1 and edition 2
      WMO FM-94 BUFR edition 3 and edition 4 
      WMO GTS abbreviated header (only decoding).
    """

    homepage = "https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home"
    url      = "https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2"

    version('2.2.0', 'b27e6f0a3eea5b92dac37372e4c45a62')

    variant('netcdf', default=True)
    variant('openjpeg', default=True)
    variant('libpng', default=True)
    variant('python', default=False)
    variant('pthreads', default=False)
    variant('openmp', default=False)
    variant('memfs', default=False)

    depends_on('netcdf', when='+netcdf')
    depends_on('openjpeg', when='+openjpeg')
    depends_on('libpng', when='+libpng')
    extends('python', when='+python')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+netcdf'):
            args.append('-DENABLE_NETCDF=ON')
        else:
            args.append('-DENABLE_NETCDF=OFF')
        if self.spec.satisfies('+openjpeg'):
            args.append('-DENABLE_JPG=ON')
        else:
            args.append('-DENABLE_JPG=OFF')
        if self.spec.satisfies('+libpng'):
            args.append('-DENABLE_PNG=ON')
        else:
            args.append('-DENABLE_PNG=OFF')
        if self.spec.satisfies('+python'):
            args.append('-DENABLE_PYTHON=ON')
        else:
            args.append('-DENABLE_PYTHON=OFF')
        if self.spec.satisfies('+pthreads'):
            args.append('-DENABLE_ECCODES_THREADS=ON')
        else:
            args.append('-DENABLE_ECCODES_THREADS=OFF')
        if self.spec.satisfies('+openmp'):
            args.append('-DENABLE_ECCODES_OMP_THREADS=ON')
        else:
            args.append('-DENABLE_ECCODES_OMP_THREADS=OFF')
        if self.spec.satisfies('+memfs'):
            args.append('-DENABLE_MEMFS=ON')
        else:
            args.append('-DENABLE_MEMFS=OFF')
        return args
