# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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
    variant('enable_quad_precision', default=True, description='Enable quad precision?')
    variant('pic', default=True, description='Generate position-independent code (PIC), useful '
                                             'for building static libraries')

    version('2022.01', sha256='a1cba1f536923f5953c28729a28e5431e127b45d6bc2c15d230939f0c02daa9b')
    version('2021.04', sha256='dcb4fe80cb3b7846f7cf89b812afff09a78a10261ea048a851f28935d6b241b1')
    version('2021.03.01', sha256='1f70e2a57f0d01e80fceb9ca9ce9661f5c1565d0437ab67618c2c4dfea0da6e9')

    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    def cmake_args(self):
        args = [
            self.define_from_variant('64BIT'),
            self.define_from_variant('GFS_PHYS'),
            self.define_from_variant('OPENMP'),
            self.define_from_variant('ENABLE_QUAD_PRECISION')
        ]

        args.append(self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc))
        args.append(self.define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx))
        args.append(self.define('CMAKE_Fortran_COMPILER', self.spec['mpi'].mpifc))

        cflags = []
        fflags = []

        if self.compiler.name in ['gcc', 'clang', 'apple-clang']:
            gfortran_major_version = int(spack.compiler.get_compiler_version_output(self.compiler.fc, '-dumpversion').split('.')[0])
            if gfortran_major_version>=10:
                fflags.append('-fallow-argument-mismatch')

        if '+pic' in self.spec:
            cflags.append(self.compiler.cc_pic_flag)
            fflags.append(self.compiler.fc_pic_flag)

        if cflags:
            args.append(self.define('CMAKE_C_FLAGS', ' '.join(cflags)))
        if fflags:
            args.append(self.define('CMAKE_Fortran_FLAGS', ' '.join(fflags)))

        return args
