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


class ParallelNetcdf(AutotoolsPackage):
    """Parallel netCDF (PnetCDF) is a library providing high-performance
    parallel I/O while still maintaining file-format compatibility with
    Unidata's NetCDF."""

    homepage = "https://trac.mcs.anl.gov/projects/parallel-netcdf"
    url      = "http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/parallel-netcdf-1.6.1.tar.gz"
    list_url = "http://cucis.ece.northwestern.edu/projects/PnetCDF/download.html"

    version('1.8.0', '825825481aa629eb82f21ca37afff1609b8eeb07')
    version('1.7.0', '267eab7b6f9dc78c4d0e6def2def3aea4bc7c9f0')
    version('1.6.1', '62a094eb952f9d1e15f07d56e535052604f1ac34')

    variant('cxx', default=True, description='Build the C++ Interface')
    variant('fortran', default=True, description='Build the Fortran Interface')
    variant('fpic', default=True,
            description='Produce position-independent code (for shared libs)')

    depends_on('mpi')

    depends_on('m4', type='build')

    # See:
    # https://trac.mcs.anl.gov/projects/parallel-netcdf/browser/trunk/INSTALL
    def configure_args(self):
        spec = self.spec

        args = ['--with-mpi={0}'.format(spec['mpi'].prefix)]

        if '+fpic' in spec:
            args.extend(['CFLAGS=-fPIC', 'CXXFLAGS=-fPIC', 'FFLAGS=-fPIC'])
        if '~cxx' in spec:
            args.append('--disable-cxx')
        if '~fortran' in spec:
            args.append('--disable-fortran')

        return args
