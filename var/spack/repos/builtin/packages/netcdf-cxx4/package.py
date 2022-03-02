# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    variant('shared', default=True, description='Enable shared library')
    # Usually the configure automatically inserts the pic flags, but we can
    # force its usage with this variant.
    variant('pic', default=True, description='Produce position-independent code (for shared libs)')
    variant('doc', default=False, description='Enable doxygen docs')

    depends_on('netcdf-c')

    depends_on('doxygen', when='+doc', type='build')

    # See https://github.com/Unidata/netcdf-cxx4/issues/109
    patch('https://github.com/Unidata/netcdf-cxx4/commit/e7cc5bab02cf089dc79616456a0a951fee979fe9.patch',
          sha256='4ddf6db9dc0c5f754cb3d68b1dbef8c385cf499f6e5df8fbccae3749336ba84a',
          when='@:4.3.1 platform=darwin')

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        if name == 'cxxflags' and '+pic' in self.spec:
            flags.append(self.compiler.cxx_pic_flag)
        elif name == 'ldlibs':
            # Address the underlinking problem reported in
            # https://github.com/Unidata/netcdf-cxx4/issues/86, which also
            # results into a linking error on macOS:
            flags.append(self.spec['netcdf-c'].libs.link_flags)

        # Note that cflags and cxxflags should be added by the compiler wrapper
        # and not on the command line to avoid overriding the default
        # compilation flags set by the configure script:
        return flags, None, None

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++4', root=self.prefix, shared=shared, recursive=True
        )

    def configure_args(self):
        config_args = self.enable_or_disable('shared')

        if '+doc' in self.spec:
            config_args.append('--enable-doxygen')
        else:
            config_args.append('--disable-doxygen')

        if self.spec.satisfies('^hdf5+mpi'):
            # The package itself does not need the MPI libraries but includes
            # <hdf5.h> (in the C code only), which requires <mpi.h> when HDF5 is
            # built with the MPI support. Using the MPI wrapper introduces
            # overlinking to MPI libraries and we would prefer not to use it but
            # it is the only reliable way to provide the compiler with the
            # correct path to <mpi.h>. For example, <mpi.h> of a MacPorts-built
            # MPICH might reside in /opt/local/include/mpich-gcc10, which Spack
            # does not know about and cannot inject with its compiler wrapper.
            config_args.append('CC={0}'.format(self.spec['mpi'].mpicc))

        return config_args

    def check(self):
        with working_dir(self.build_directory):
            make('check', parallel=False)
