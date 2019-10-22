# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetcdfCxx4(AutotoolsPackage):
    """C++ interface for NetCDF4"""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "https://www.github.com/unidata/netcdf-cxx4/tarball/v4.3.0"

    version('4.3.0', sha256='f4766d5a19c91093be80ddd2eaf1fbbd8d203854cc69fc73d2ad293b099ac799')

    # Usually the configure automatically inserts the pic flags, but we can
    # force its usage with this variant.
    variant('pic', default=True, description='Produce position-independent code (for shared libs)')

    depends_on('netcdf')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    force_autoreconf = True

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)
        elif name == 'cppflags':
            flags.append('-I' + self.spec['netcdf'].prefix.include)

        return (None, None, flags)

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++4', root=self.prefix, shared=shared, recursive=True
        )
