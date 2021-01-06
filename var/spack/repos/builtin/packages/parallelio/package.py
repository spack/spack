# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Parallelio(CMakePackage):
    """The Parallel IO libraries (PIO) are high-level parallel I/O C and
    Fortran libraries for applications that need to do netCDF I/O from
    large numbers of processors on a HPC system."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url      = "https://github.com/NCAR/ParallelIO/archive/pio2_5_2.tar.gz"

    maintainers = ['tkameyama']

    version('2_5_2', sha256='935bc120ef3bf4fe09fb8bfdf788d05fb201a125d7346bf6b09e27ac3b5f345c')

    variant('pnetcdf', default=False, description='enable pnetcdf')

    depends_on('mpi')
    depends_on('netcdf-c +mpi', type='link')
    depends_on('netcdf-fortran', type='link')
    depends_on('parallel-netcdf', type='link', when='+pnetcdf')

    def cmake_args(self):
        define = self.define
        spec = self.spec
        env['CC'] = spec['mpi'].mpicc
        env['FC'] = spec['mpi'].mpifc
        args = [
            define('NetCDF_C_PATH', spec['netcdf-c'].prefix),
            define('NetCDF_Fortran_PATH', spec['netcdf-fortran'].prefix),
        ]
        if spec.satisfies('+pnetcdf'):
            args.extend([
                define('PnetCDF_C_PATH', spec['parallel-netcdf'].prefix),
                define('PnetCDF_Fortran_PATH', spec['parallel-netcdf'].prefix),
            ])
        return args
