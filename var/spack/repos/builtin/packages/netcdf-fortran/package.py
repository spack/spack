# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetcdfFortran(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the Fortran
    distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url      = "https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.5.2.tar.gz"

    version('4.5.2', sha256='b959937d7d9045184e9d2040a915d94a7f4d0185f4a9dceb8f08c94b0c3304aa')
    version('4.4.5', sha256='2467536ce29daea348c736476aa8e684c075d2f6cab12f3361885cb6905717b8')
    version('4.4.4', sha256='b2d395175f8d283e68c8be516e231a96b191ade67ad0caafaf7fa01b1e6b5d75')
    version('4.4.3', sha256='330373aa163d5931e475b5e83da5c1ad041e855185f24e6a8b85d73b48d6cda9')

    variant('mpi', default=True,
            description='Enable parallel I/O for netcdf-4')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    # We need to build with MPI wrappers if parallel I/O features is enabled:
    # https://www.unidata.ucar.edu/software/netcdf/docs/building_netcdf_fortran.html
    depends_on('mpi', when='+mpi')

    depends_on('netcdf-c~mpi', when='~mpi')
    depends_on('netcdf-c+mpi', when='+mpi')

    # The default libtool.m4 is too old to handle NAG compiler properly:
    # https://github.com/Unidata/netcdf-fortran/issues/94
    patch('nag.patch', when='@:4.4.4%nag')

    # Parallel builds do not work in the fortran directory. This patch is
    # derived from https://github.com/Unidata/netcdf-fortran/pull/211
    patch('no_parallel_build.patch', when='@4.5.2')

    def flag_handler(self, name, flags):
        if name in ['cflags', 'fflags'] and '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)
        elif name == 'cppflags':
            flags.append(self.spec['netcdf-c'].headers.cpp_flags)
        elif name == 'ldflags':
            # We need to specify LDFLAGS to get correct dependency_libs
            # in libnetcdff.la, so packages that use libtool for linking
            # could correctly link to all the dependencies even when the
            # building takes place outside of Spack environment, i.e.
            # without Spack's compiler wrappers.
            flags.append(self.spec['netcdf-c'].libs.search_flags)

        return None, None, flags

    @property
    def libs(self):
        libraries = ['libnetcdff']

        # This package installs both shared and static libraries. Permit
        # clients to query which one they want.
        query_parameters = self.spec.last_query.extra_parameters
        shared = 'shared' in query_parameters

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    def configure_args(self):
        config_args = []

        if '+mpi' in self.spec:
            config_args.append('CC=%s' % self.spec['mpi'].mpicc)
            config_args.append('FC=%s' % self.spec['mpi'].mpifc)
            config_args.append('F77=%s' % self.spec['mpi'].mpif77)

        return config_args
