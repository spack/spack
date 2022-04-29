# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Fms(CMakePackage):
    """GFDL's Flexible Modeling System (FMS) is a software environment
    that supports the efficient development, construction, execution,
    and scientific interpretation of atmospheric, oceanic, and climate
    system models."""

    homepage = "https://github.com/NOAA-GFDL/FMS"
    url      = "https://github.com/NOAA-GFDL/FMS/archive/refs/tags/2021.02.01.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    variant('64bit', default=True, description='64 bit?')
    variant('gfs_phys', default=True, description='Use GFS Physics?')
    variant('openmp', default=True, description='Use OpenMP?')

    version('2021.04', sha256='dcb4fe80cb3b7846f7cf89b812afff09a78a10261ea048a851f28935d6b241b1')
    version('2021.03.01', sha256='1f70e2a57f0d01e80fceb9ca9ce9661f5c1565d0437ab67618c2c4dfea0da6e9')

    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    def cmake_args(self):
        args = [
            self.define_from_variant('64BIT'),
            self.define_from_variant('GFS_PHYS'),
            self.define_from_variant('OPENMP')
        ]

        args.append(self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc))
        args.append(self.define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx))
        args.append(self.define('CMAKE_Fortran_COMPILER', self.spec['mpi'].mpifc))

        return args
