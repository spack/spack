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


class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent
    data formats that support the creation, access, and sharing of array-oriented
    scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.4.0', 'cffda0cbd97fdb3a06e9274f7aef438e')
    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('mpi',  default=True,  description='Enables MPI parallelism')
    variant('hdf4', default=False, description='Enable HDF4 support')

    depends_on("m4")
    depends_on("hdf", when='+hdf4')

    # Required for DAP support
    depends_on("curl")

    # Required for NetCDF-4 support
    depends_on("zlib")
    depends_on("hdf5+mpi", when='+mpi')
    depends_on("hdf5~mpi", when='~mpi')

    def install(self, spec, prefix):
        # Environment variables
        CPPFLAGS = []
        LDFLAGS  = []
        LIBS     = []

        config_args = [
            "--prefix=%s" % prefix,
            "--enable-fsync",
            "--enable-v2",
            "--enable-utilities",
            "--enable-shared",
            "--enable-static",
            "--enable-largefile",
            # necessary for HDF5 support
            "--enable-netcdf-4",
            "--enable-dynamic-loading",
            # necessary for DAP support
            "--enable-dap"
        ]

        # Make sure Netcdf links against Spack's curl
        # Otherwise it may pick up system's curl, which could lead to link errors:
        # /usr/lib/x86_64-linux-gnu/libcurl.so: undefined reference to `SSL_CTX_use_certificate_chain_file@OPENSSL_1.0.0'
        LIBS.append("-lcurl")
        CPPFLAGS.append("-I%s" % spec['curl'].prefix.include)
        LDFLAGS.append( "-L%s" % spec['curl'].prefix.lib)

        if '+mpi' in spec:
            config_args.append('--enable-parallel4')

        CPPFLAGS.append("-I%s/include" % spec['hdf5'].prefix)
        LDFLAGS.append( "-L%s/lib"     % spec['hdf5'].prefix)

        # HDF4 support
        # As of NetCDF 4.1.3, "--with-hdf4=..." is no longer a valid option
        # You must use the environment variables CPPFLAGS and LDFLAGS
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")
            CPPFLAGS.append("-I%s/include" % spec['hdf'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['hdf'].prefix)
            LIBS.append(    "-l%s"         % "jpeg")

        if 'szip' in spec:
            CPPFLAGS.append("-I%s/include" % spec['szip'].prefix)
            LDFLAGS.append( "-L%s/lib"     % spec['szip'].prefix)
            LIBS.append(    "-l%s"         % "sz")

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CPPFLAGS=%s' % ' '.join(CPPFLAGS))
        config_args.append('LDFLAGS=%s'  % ' '.join(LDFLAGS))
        config_args.append('LIBS=%s'     % ' '.join(LIBS))

        configure(*config_args)
        make()
        make("install")
