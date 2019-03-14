# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetcdfCxx(AutotoolsPackage):
    """Deprecated C++ compatibility bindings for NetCDF.
    These do NOT read or write NetCDF-4 files, and are no longer
    maintained by Unidata.  Developers should migrate to current
    NetCDF C++ bindings, in Spack package netcdf-cxx4."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx-4.2.tar.gz"

    version('4.2', 'd32b20c00f144ae6565d9e98d9f6204c')

    depends_on('netcdf')

    variant(
        'netcdf4', default=True, description='Compile with netCDF4 support')

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++', root=self.prefix, shared=shared, recursive=True
        )

    def flag_handler(self, name, flags):
        # Add netCDF4 support via the USE_NETCDF4 macro
        if name == 'cflags' and '+netcdf4' in self.spec:
            flags.append('-DUSE_NETCDF4')
        if name == 'cppflags' and '+netcdf4' in self.spec:
            flags.append('-DUSE_NETCDF4')
        return (None, None, flags)
