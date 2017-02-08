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


class Netcdf(AutotoolsPackage):
    """NetCDF is a set of software libraries and self-describing,
    machine-independent data formats that support the creation, access,
    and sharing of array-oriented scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.gfd-dennou.org/arch/netcdf/unidata-mirror/netcdf-4.3.3.tar.gz"

    # Version 4.4.1.1 is having problems in tests
    #    https://github.com/Unidata/netcdf-c/issues/343 
    version('4.4.1.1', '503a2d6b6035d116ed53b1d80c811bda')
    # netcdf@4.4.1 can crash on you (in real life and in tests).  See:
    #    https://github.com/Unidata/netcdf-c/issues/282
    version('4.4.1',   '7843e35b661c99e1d49e60791d5072d8')
    version('4.4.0',   'cffda0cbd97fdb3a06e9274f7aef438e')
    version('4.3.3.1', '5c9dad3705a3408d27f696e5b31fb88c')
    version('4.3.3',   '5fbd0e108a54bd82cb5702a73f56d2ae')

    variant('mpi',     default=True,  description='Enables MPI parallelism')
    variant('hdf4',    default=False, description='Enable HDF4 support')
    variant('shared',  default=True,  description='Enable shared library')
    variant('parallel-netcdf', default=False, description='Enable PnetCDF support')
    variant('dap',     default=False, description='Enable DAP support')
    variant('cdmremote', default=False, description='Enable CDM Remote support')
    # These variants control the number of dimensions (i.e. coordinates and
    # attributes) and variables (e.g. time, entity ID, number of coordinates)
    # that can be used in any particular NetCDF file.
    variant('maxdims', default=1024,
            description='Defines the maximum dimensions of NetCDF files.')
    variant('maxvars', default=8192,
            description='Defines the maximum variables of NetCDF files.')

    depends_on("m4", type='build')
    depends_on("hdf", when='+hdf4')
    depends_on("curl@7.18.0:", when='+dap')
    depends_on("curl@7.18.0:", when='+cdmremote')
    depends_on('parallel-netcdf', when='@4.2.1.1:+parallel-netcdf')

    # Required for NetCDF-4 support
    depends_on("zlib@1.2.5:")
    depends_on('hdf5')

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250
    depends_on('hdf5@:1.8', when='@:4.4.0')

    def patch(self):
        try:
            max_dims = int(self.spec.variants['maxdims'].value)
            max_vars = int(self.spec.variants['maxvars'].value)
        except (ValueError, TypeError):
            raise TypeError('NetCDF variant values max[dims|vars] must be '
                            'integer values.')

        ff = FileFilter(join_path('include', 'netcdf.h'))
        ff.filter(r'^(#define\s+NC_MAX_DIMS\s+)\d+(.*)$',
                  r'\1{0}\2'.format(max_dims))
        ff.filter(r'^(#define\s+NC_MAX_VARS\s+)\d+(.*)$',
                  r'\1{0}\2'.format(max_vars))

    def configure_args(self):
        spec = self.spec
        # Workaround until variant forwarding works properly
        if '+mpi' in spec and spec.satisfies('^hdf5~mpi'):
            raise RuntimeError('Invalid spec. Package netcdf requires '
                               'hdf5+mpi, but spec asked for hdf5~mpi.')

        # Environment variables
        CFLAGS   = []
        CPPFLAGS = []
        LDFLAGS  = []
        LIBS     = []

        config_args = [
            "--enable-fsync",
            "--enable-v2",
            "--enable-utilities",
            "--enable-static",
            "--enable-largefile",
            # necessary for HDF5 support
            "--enable-netcdf-4",
            "--enable-dynamic-loading",
        ]

        if '+shared' in spec:
            config_args.append('--enable-shared')
        else:
            config_args.append('--disable-shared')
            # We don't have shared libraries but we still want it to be
            # possible to use this library in shared builds
            CFLAGS.append('-fPIC')

        if '+dap' in spec:
            config_args.append('--enable-dap')
        else:
            config_args.append('--disable-dap')

        if '+cdmremote' in spec:
            config_args.append('--enable-cdmremote')
        else:
            config_args.append('--disable-cdmremote')

        if '+dap' in spec or '+cdmremote' in spec:
            # Make sure Netcdf links against Spack's curl, otherwise it may
            # pick up system's curl, which can give link errors, e.g.:
            #   undefined reference to `SSL_CTX_use_certificate_chain_file`
            LIBS.append("-lcurl")
            CPPFLAGS.append("-I%s" % spec['curl'].prefix.include)
            LDFLAGS.append("-L%s" % spec['curl'].prefix.lib)

        if '+mpi' in spec:
            config_args.append('--enable-parallel4')

        CPPFLAGS.append("-I%s/include" % spec['hdf5'].prefix)
        LDFLAGS.append("-L%s/lib"     % spec['hdf5'].prefix)

        # HDF4 support
        # As of NetCDF 4.1.3, "--with-hdf4=..." is no longer a valid option
        # You must use the environment variables CPPFLAGS and LDFLAGS
        if '+hdf4' in spec:
            config_args.append("--enable-hdf4")
            CPPFLAGS.append("-I%s/include" % spec['hdf'].prefix)
            LDFLAGS.append("-L%s/lib"     % spec['hdf'].prefix)
            LIBS.append("-l%s"         % "jpeg")

        if '+szip' in spec:
            CPPFLAGS.append("-I%s/include" % spec['szip'].prefix)
            LDFLAGS.append("-L%s/lib"     % spec['szip'].prefix)
            LIBS.append("-l%s"         % "sz")

        # PnetCDF support
        if '+parallel-netcdf' in spec:
            config_args.append('--enable-pnetcdf')
            config_args.append('CC=%s' % spec['mpi'].mpicc)
            CPPFLAGS.append("-I%s/include" % spec['parallel-netcdf'].prefix)
            LDFLAGS.append("-L%s/lib"      % spec['parallel-netcdf'].prefix)

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CFLAGS=%s'   % ' '.join(CFLAGS))
        config_args.append('CPPFLAGS=%s' % ' '.join(CPPFLAGS))
        config_args.append('LDFLAGS=%s'  % ' '.join(LDFLAGS))
        config_args.append('LIBS=%s'     % ' '.join(LIBS))

        return config_args

    def check(self):
        # h5_test fails when run in parallel
        make('check', parallel=False)
