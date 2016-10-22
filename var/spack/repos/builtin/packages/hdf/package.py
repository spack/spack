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


class Hdf(Package):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://www.hdfgroup.org/products/hdf4/"
    url      = "https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.11/src/hdf-4.2.11.tar.gz"
    list_url = "https://www.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 3

    version('4.2.12', '79fd1454c899c05e34a3da0456ab0c1c')
    version('4.2.11', '063f9928f3a19cc21367b71c3b8bbf19')

    variant('szip', default=False, description="Enable szip support")

    depends_on('jpeg@6b:')
    depends_on('szip', when='+szip')
    depends_on('zlib@1.1.4:')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')

    def install(self, spec, prefix):
        config_args = [
            'CFLAGS=-fPIC',
            '--prefix={0}'.format(prefix),
            '--with-jpeg={0}'.format(spec['jpeg'].prefix),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
            '--disable-netcdf',  # must be disabled to build NetCDF with HDF4
            '--enable-fortran',
            '--disable-shared',  # fortran and shared libs are not compatible
            '--enable-static',
            '--enable-production'
        ]

        # Szip support
        if '+szip' in spec:
            config_args.append('--with-szlib={0}'.format(spec['szip'].prefix))
        else:
            config_args.append('--without-szlib')

        configure(*config_args)

        make()

        if self.run_tests:
            make('check')

        make('install')
