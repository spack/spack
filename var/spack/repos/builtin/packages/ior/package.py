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
import os


class Ior(Package):
    """The IOR software is used for benchmarking parallel file systems
    using POSIX, MPI-IO, or HDF5 interfaces."""

    homepage = "https://github.com/LLNL/ior"
    url      = "https://github.com/LLNL/ior/archive/3.0.1.tar.gz"

    version('3.0.1', '71150025e0bb6ea1761150f48b553065')

    variant('hdf5',  default=False, description='support IO with HDF5 backend')
    variant('ncmpi', default=False, description='support IO with NCMPI backend')

    depends_on('mpi')
    depends_on('hdf5+mpi',   when='+hdf5')
    depends_on('parallel-netcdf', when='+ncmpi')

    def install(self, spec, prefix):
        os.system('./bootstrap')

        config_args = [
            'MPICC=%s' % spec['mpi'].prefix.bin + '/mpicc',
            '--prefix=%s' % prefix,
        ]

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')
            config_args.append('CFLAGS=-D H5_USE_16_API')
        else:
            config_args.append('--without-hdf5')

        if '+ncmpi' in spec:
            config_args.append('--with-ncmpi')
        else:
            config_args.append('--without-ncmpi')

        configure(*config_args)

        make()
        make('install')
