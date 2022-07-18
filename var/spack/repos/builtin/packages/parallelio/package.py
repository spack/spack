# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Parallelio(CMakePackage):
    """The Parallel IO libraries (PIO) are high-level parallel I/O C and
    Fortran libraries for applications that need to do netCDF I/O from
    large numbers of processors on a HPC system."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url      = "https://github.com/NCAR/ParallelIO/archive/pio2_5_4.tar.gz"

    maintainers = ['tkameyama']

    version('2.5.7', sha256='af8af04e41af17f98f2c90b996ef0d8bcd980377e0b35e57b38938c7fdc87cbd')
    version('2.5.4', sha256='e51dc71683da808a714deddc1a80c2650ce847110383e42f1710f3ba567e7a65')
    version('2.5.3', sha256='205a0a128fd5262700efc230b3380dc5ab10e74bc5d273ae05db76c9d95487ca')
    version('2.5.2', sha256='935bc120ef3bf4fe09fb8bfdf788d05fb201a125d7346bf6b09e27ac3b5f345c')

    variant('pnetcdf', default=False, description='enable pnetcdf')
    variant('timing', default=False, description='enable GPTL timing')
    variant('shared', default=True, description='Build shared libraries')

    patch('remove_redefinition_of_mpi_offset.patch', when='@:2.5.6')

    depends_on('mpi')
    depends_on('netcdf-c +mpi', type='link')
    depends_on('netcdf-fortran', type='link')
    depends_on('parallel-netcdf', type='link', when='+pnetcdf')

    resource(name='CMake_Fortran_utils',
             git='https://github.com/CESM-Development/CMake_Fortran_utils.git',
             tag='master')

    resource(name='genf90',
             git='https://github.com/PARALLELIO/genf90.git',
             tag='genf90_200608')

    def url_for_version(self, version):
        url = 'https://github.com/NCAR/ParallelIO/archive/refs/tags/pio{}.tar.gz'
        return url.format(version.underscored)

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        env['CC'] = spec['mpi'].mpicc
        env['FC'] = spec['mpi'].mpifc
        src = self.stage.source_path
        args = [
            define('NetCDF_C_PATH', spec['netcdf-c'].prefix),
            define('NetCDF_Fortran_PATH', spec['netcdf-fortran'].prefix),
            define('USER_CMAKE_MODULE_PATH', join_path(src, 'CMake_Fortran_utils')),
            define('GENF90_PATH', join_path(src, 'genf90')),
            define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]
        if spec.satisfies('+pnetcdf'):
            args.extend([
                define('PnetCDF_C_PATH', spec['parallel-netcdf'].prefix),
                define('PnetCDF_Fortran_PATH', spec['parallel-netcdf'].prefix),
            ])
        args.extend([
            define_from_variant('PIO_ENABLE_TIMING', 'timing'),
        ])
        # Compatibility flags for gfortran
        fflags = []
        if self.compiler.name in ['gcc', 'clang', 'apple-clang']:
            gfortran_major_ver = int(spack.compiler.get_compiler_version_output(
                                     self.compiler.fc, '-dumpversion').split('.')[0])
            if gfortran_major_ver >= 10:
                fflags.append('-fallow-argument-mismatch')
        if fflags:
            args.extend([
                self.define('CMAKE_Fortran_FLAGS', ' '.join(fflags))
            ])
        return args
