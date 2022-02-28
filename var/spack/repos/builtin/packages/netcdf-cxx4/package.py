# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class NetcdfCxx4(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C++ distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx4-4.3.1.tar.gz"

    maintainers = ['WardF']

    version('4.3.1', sha256='6a1189a181eed043b5859e15d5c080c30d0e107406fbb212c8fb9814e90f3445')
    version('4.3.0', sha256='e34fbc6aba243ec82c23e9ee99db2430555ada849c54c1f3ab081b0ddd0f5f30')

    # Usually the configure automatically inserts the pic flags, but we can
    # force its usage with this variant.
    variant('static', default=True, description='Enable building static libraries')
    variant('shared', default=True, description='Enable shared library')
    variant('pic', default=True, description='Produce position-independent code (for shared libs)')
    variant('doc', default=False, description='Enable doxygen docs')

    depends_on('netcdf-c')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('doxygen', when='+doc', type='build')

    conflicts('~shared', when='~static')

    force_autoreconf = True

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        elif name == 'cppflags':
            flags.append('-I' + self.spec['netcdf-c'].prefix.include)
        elif name == 'ldflags':
            # We need to specify LDFLAGS to get correct dependency_libs
            # in libnetcdf_c++.la, so packages that use libtool for linking
            # can correctly link to all the dependencies even when the
            # building takes place outside of Spack environment, i.e.
            # without Spack's compiler wrappers.
            config_flags = [self.spec['netcdf-c'].libs.search_flags]
            # On macOS, we also need to add this to ldflags
            if self.spec.satisfies("platform=darwin"):
                flags = [self.spec['netcdf-c'].libs.search_flags, 
                         self.spec['netcdf-c'].libs.link_flags] + flags
        return (None, None, flags)

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++4', root=self.prefix, shared=shared, recursive=True
        )

    def configure_args(self):
        config_args = []

        # We need to build with MPI wrappers if either of the parallel I/O
        # features is enabled in netcdf-c:
        # https://www.unidata.ucar.edu/software/netcdf/docs/building_netcdf_fortran.html
        netcdf_c_spec = self.spec['netcdf-c']
        if '+mpi' in netcdf_c_spec or '+parallel-netcdf' in netcdf_c_spec:
            config_args.append('CC=%s' % self.spec['mpi'].mpicc)
            config_args.append('FC=%s' % self.spec['mpi'].mpifc)
            config_args.append('F77=%s' % self.spec['mpi'].mpif77)

        if '+static' in self.spec:
            config_args.append('--enable-static')
        else:
            config_args.append('--disable-static')

        if '+shared' in self.spec:
            config_args.append('--enable-shared')
        else:
            config_args.append('--disable-shared')

        if '+pic' in self.spec:
            config_args.append('--with-pic')
        else:
            config_args.append('--without-pic')

        if '+doc' in self.spec:
            config_args.append('--enable-doxygen')
        else:
            config_args.append('--disable-doxygen')

        return config_args

    @when('@:4.3.1')
    def build(self, spec, prefix):
        if spec.satisfies("platform=darwin"):
            # If on macos, rename the file "VERSION" so it doesn't collide with the
            # c++ include file (named "version"). Note this collision occurs since macos
            # uses a case-insensitive file system.
            #
            # Unidata has fixed this in their development track:
            #   https://github.com/Unidata/netcdf-cxx4/commit/41c0233cb964a3ee1d4e5db5448cd28d617925fb
            os.rename('VERSION', 'config.VERSION')
        super(NetcdfCxx4, self).build(spec, prefix)
