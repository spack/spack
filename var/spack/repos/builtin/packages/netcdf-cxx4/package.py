# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetcdfCxx4(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C++ distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url      = "https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-4.3.1.tar.gz"

    version('4.3.1', sha256='6a1189a181eed043b5859e15d5c080c30d0e107406fbb212c8fb9814e90f3445')
    version('4.3.0', sha256='f4766d5a19c91093be80ddd2eaf1fbbd8d203854cc69fc73d2ad293b099ac799')

    # Usually the configure automatically inserts the pic flags, but we can
    # force its usage with this variant.
    variant('pic', default=True, description='Produce position-independent code (for shared libs)')

    depends_on('netcdf-c')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    force_autoreconf = True

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)
        elif name == 'cppflags':
            flags.append('-I' + self.spec['netcdf-c'].prefix.include)

        return (None, None, flags)

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++4', root=self.prefix, shared=shared, recursive=True
        )
