# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ParallelNetcdf(AutotoolsPackage):
    """Parallel netCDF (PnetCDF) is a library providing high-performance
    parallel I/O while still maintaining file-format compatibility with
    Unidata's NetCDF."""

    homepage = "https://trac.mcs.anl.gov/projects/parallel-netcdf"
    url      = "http://cucis.ece.northwestern.edu/projects/PnetCDF/Release/parallel-netcdf-1.6.1.tar.gz"
    list_url = "http://cucis.ece.northwestern.edu/projects/PnetCDF/download.html"

    version('1.8.0', '825825481aa629eb82f21ca37afff1609b8eeb07')
    version('1.7.0', '267eab7b6f9dc78c4d0e6def2def3aea4bc7c9f0')
    version('1.6.1', '62a094eb952f9d1e15f07d56e535052604f1ac34')

    variant('cxx', default=True, description='Build the C++ Interface')
    variant('fortran', default=True, description='Build the Fortran Interface')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    depends_on('mpi')

    depends_on('m4', type='build')

    # See:
    # https://trac.mcs.anl.gov/projects/parallel-netcdf/browser/trunk/INSTALL
    def configure_args(self):
        spec = self.spec

        args = ['--with-mpi={0}'.format(spec['mpi'].prefix)]
        args.append('MPICC={0}'.format(spec['mpi'].mpicc))
        args.append('MPICXX={0}'.format(spec['mpi'].mpicxx))
        args.append('MPIF77={0}'.format(spec['mpi'].mpifc))
        args.append('MPIF90={0}'.format(spec['mpi'].mpifc))
        args.append('SEQ_CC={0}'.format(spack_cc))

        if '+pic' in spec:
            args.extend([
                'CFLAGS={0}'.format(self.compiler.pic_flag),
                'CXXFLAGS={0}'.format(self.compiler.pic_flag),
                'FFLAGS={0}'.format(self.compiler.pic_flag)
            ])

        if '~cxx' in spec:
            args.append('--disable-cxx')

        if '~fortran' in spec:
            args.append('--disable-fortran')

        return args

    def install(self, spec, prefix):
        # Installation fails in parallel
        make('install', parallel=False)
